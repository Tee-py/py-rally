from dataclasses import dataclass
from datetime import datetime

import requests
from eth_abi import encode

from py_rally.abis import FORWARDER_ABI, RELAY_HUB_ABI
from py_rally.config import NetworkConfig
from py_rally.constants import OK_RESPONSE
from py_rally.custom_types import Account, GSNServerConfigPayload, GSNTransaction, RelayHttpRequest, RelayRequest
from py_rally.exceptions import RallyAPIError
from py_rally.helpers import calculate_call_data_cost, estimate_gas_without_call_data, sign_relay_request


@dataclass
class RallyGSNClient:
    config: NetworkConfig

    @property
    def auth_header(self):
        return {'Authorization': f'Bearer {self.config.relayer_api_key}'}

    def _update_config(self, txn: GSNTransaction) -> None:
        response = requests.get(
            f'{self.config.gsn_config.relay_url}/getaddr',
            headers=self.auth_header,
        )
        if response.status_code != OK_RESPONSE:
            raise RallyAPIError(f'Failed to fetch config from API: {response.text}')
        server_config: GSNServerConfigPayload = response.json()
        self.config.gsn_config.relay_worker_address = server_config['relayWorkerAddress']
        # Update Txn Fee per Gas
        suggested_min_priority_fee = server_config['minMaxPriorityFeePerGas']
        padded = round(int(suggested_min_priority_fee) * 1.4)
        txn['max_priority_fee_per_gas'] = str(padded)
        if server_config['chainId'] == '8001':
            txn['max_fee_per_gas'] = str(padded)
        else:
            txn['max_fee_per_gas'] = server_config['maxMaxFeePerGas']

    def _get_account_nonce(self, account: Account) -> str:
        forwarder_address = self.config.web3.to_checksum_address(
            self.config.gsn_config.forwarder_address,
        )
        forwarder_contract = self.config.web3.eth.contract(
            forwarder_address,
            abi=FORWARDER_ABI,
        )
        nonce = forwarder_contract.functions.getNonce(account.address).call()
        return str(nonce)

    def _estimate_call_data_cost_for_request(
        self,
        request_payload: RelayRequest,
    ) -> str:
        request_copy = request_payload.copy()
        request_copy['relayData']['transactionCallDataGasUsed'] = '0xffffffffff'
        request_copy['relayData']['paymasterData'] = '0x' + 'ff' * self.config.gsn_config.max_paymaster_data_length
        max_acceptance_budget = '0xffffffffff'
        signature = '0x' + 'ff' * 65
        approval_data = '0x' + 'ff' * self.config.gsn_config.max_approval_data_length
        relay_hub_address = self.config.web3.to_checksum_address(
            self.config.gsn_config.relay_hub_address,
        )
        relay_hub = self.config.web3.eth.contract(relay_hub_address, abi=RELAY_HUB_ABI)

        txn = relay_hub.functions.relayCall(
            self.config.gsn_config.domain_separator_name,
            max_acceptance_budget,
            request_copy,
            signature,
            approval_data,
        ).buildTransaction()
        cost = calculate_call_data_cost(
            txn,
            self.config.gsn_config.gtx_data_non_zero,
            self.config.gsn_config.gtx_data_zero,
        )
        return hex(cost)

    def _build_relay_request(
        self,
        txn: GSNTransaction,
        account: Account,
    ) -> RelayRequest:
        txn['gas'] = estimate_gas_without_call_data(
            txn,
            self.config.gsn_config.gtx_data_non_zero,
            self.config.gsn_config.gtx_data_zero,
        )
        txn_expiry = round(
            datetime.now().timestamp() + self.config.gsn_config.request_valid_seconds,
        )
        sender_nonce = self._get_account_nonce(account)

        relay_request: RelayRequest = {
            'request': {
                'from': txn['from_address'],
                'to': txn['to'],
                'value': str(txn['value']),
                'gas': str(int(txn['gas'], 16)),
                'nonce': sender_nonce,
                'data': txn['data'],
                'validUntilTime': str(txn_expiry),
            },
            'relayData': {
                'maxFeePerGas': txn['max_fee_per_gas'],
                'maxPriorityFeePerGas': txn['max_priority_fee_per_gas'],
                'transactionCalldataGasUsed': '',
                'relayWorker': self.config.gsn_config.relay_worker_address,
                'paymaster': self.config.gsn_config.paymaster_address,
                'forwarder': self.config.gsn_config.forwarder_address,
                'paymasterData': txn['paymaster_data'],
                'clientId': '1',
            },
        }
        call_data_gas = self._estimate_call_data_cost_for_request(relay_request)
        relay_request['relayData']['transactionCalldataGasUsed'] = str(int(call_data_gas, 16))
        return relay_request

    def _build_relay_http_request(self, relay_request: RelayRequest, account: Account) -> RelayHttpRequest:
        signature = sign_relay_request(
            relay_request,
            self.config.gsn_config.domain_separator_name,
            self.config.gsn_config.chain_id,
            account,
        )
        # get the transaction count of an address
        relay_worker_address = self.config.web3.to_checksum_address(relay_request['relayData']['relayWorker'])
        relay_last_nonce = self.config.web3.eth.get_transaction_count(relay_worker_address)
        relay_max_nonce = relay_last_nonce + self.config.gsn_config.max_relay_nonce_gap
        metadata = {
            'maxAcceptanceBudget': self.config.gsn_config.max_acceptance_budget,
            'relayHubAddress': self.config.gsn_config.relay_hub_address,
            'signature': signature,
            'approvalData': '0x',
            'relayMaxNonce': relay_max_nonce,
            'relayLastKnownNonce': relay_last_nonce,
            'domainSeparatorName': self.config.gsn_config.domain_separator_name,
            'relayRequestId': '',
        }
        return {
            'relayRequest': relay_request,
            'metadata': metadata,
        }

    def _get_relay_request_id(self, relay_request: RelayRequest, signature: str):
        types = ['address', 'uint256', 'bytes']
        parameters = [
            relay_request['request']['from'],
            relay_request['request']['nonce'],
            bytes.fromhex(signature[2:]),
        ]
        encoded = encode(types, parameters)
        hash_value = self.config.web3.keccak(hexstr=f'0x{encoded.hex()}').hex()
        raw_rly_request_id = hash_value.replace('0x', '').zfill(64)

        prefix_size = 8
        prefixed_request_id = raw_rly_request_id.replace(raw_rly_request_id[:prefix_size], '0' * prefix_size)
        return f'0x{prefixed_request_id}'

    def relay_transaction(self, account: Account, txn: GSNTransaction):
        self._update_config(txn)
        relay_request = self._build_relay_request(txn, account)
        http_request = self._build_relay_http_request(relay_request, account)
        request_id = self._get_relay_request_id(relay_request, http_request['metadata']['signature'])
        http_request['metadata']['relayRequestId'] = request_id
        requests.post(
            f'{self.config.gsn_config.relay_url}/relay',
            data=http_request,
            headers=self.auth_header,
        )
