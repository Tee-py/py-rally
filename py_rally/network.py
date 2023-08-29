from dataclasses import dataclass

from py_rally.gsn import RallyGSNClient
from py_rally.abis import TOKEN_FAUCET_ABI
from py_rally.custom_types import Account, GSNTransaction, MetaTxMethod
from py_rally.exceptions import NetworkClientError
from py_rally.helpers import get_execute_meta_transaction_txn, get_permit_txn, get_token_balance


@dataclass
class RallyNetworkClient:
    gsn_client: RallyGSNClient

    def _get_rly_claim_txn_for_account(self, account: Account):
        token_faucet_address = self.gsn_client.config.web3.to_checksum_address(
            self.gsn_client.config.contracts['faucet'],
        )
        token_faucet_contract = self.gsn_client.config.web3.eth.contract(token_faucet_address, abi=TOKEN_FAUCET_ABI)
        tx = token_faucet_contract.functions.claim().build_transaction({'from': account.address})
        gsn_txn: GSNTransaction = {
            'from_address': tx['from'],
            'to': tx['to'],
            'data': tx['data'],
            'max_fee_per_gas': hex(tx['maxFeePerGas']),
            'max_priority_fee_per_gas': hex(tx['maxPriorityFeePerGas']),
            'gas': hex(tx['gas']),
            'value': tx['value'],
            'paymaster_data': '0x',
            'client_id': 1,
        }
        return gsn_txn

    def _get_token_transfer_txn(
        self,
        account: Account,
        to: str,
        amount: float,
        erc20_token: str,
        meta_tx_method: MetaTxMethod,
    ) -> GSNTransaction:
        if meta_tx_method == MetaTxMethod.Permit:
            transfer_txn = get_permit_txn(
                self.gsn_client.config.web3,
                account,
                self.gsn_client.config.gsn_config.paymaster_address,
                to,
                amount,
                erc20_token,
                self.gsn_client.config.gsn_config.chain_id,
            )
        else:
            transfer_txn = get_execute_meta_transaction_txn(
                self.gsn_client.config.web3,
                account,
                to,
                amount,
                erc20_token,
                str(self.gsn_client.config.gsn_config.chain_id),
            )
        return transfer_txn

    def set_api_key(self, api_key: str):
        self.gsn_client.config.relayer_api_key = api_key

    def claim_rally(self, account: Account):
        claim_txn = self._get_rly_claim_txn_for_account(account)
        return self.relay_transaction(account, claim_txn)

    def token_transfer(
        self,
        account: Account,
        to: str,
        amount: float,
        erc20_token: str,
        meta_tx_method: MetaTxMethod,
    ):
        account_balance = get_token_balance(self.gsn_client.config.web3, erc20_token, account)
        if (account_balance - amount) < 0:
            raise NetworkClientError('Insufficient balance to execute transfer')
        transfer_txn = self._get_token_transfer_txn(
            account,
            to,
            amount,
            erc20_token,
            meta_tx_method,
        )
        self.relay_transaction(account, transfer_txn)

    def relay_transaction(self, signer: Account, txn: GSNTransaction):
        return self.gsn_client.submit_transaction(signer, txn)
