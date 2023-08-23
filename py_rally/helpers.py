from typing import Dict, Tuple

from eth_account.messages import encode_structured_data
from web3 import Web3

from py_rally.constants import DOMAIN_SEPARATOR_VERSION, EIP712TYPE, RELAY_DATA_SIGNED_TYPE, RELAY_REQUEST_SIGNED_TYPE
from py_rally.custom_types import Account, EIP721DomainType, GSNTransaction, RelayRequest


def calculate_zero_non_zero_bytes_from_data(data: str) -> Tuple[int, int]:
    zero_bytes = 0
    non_zero_bytes = 0
    bytes_str = bytes.fromhex(data.replace('0x', ''))
    for char in bytes_str:
        if char == 0:
            zero_bytes += 1
        else:
            non_zero_bytes += 1
    return zero_bytes, non_zero_bytes


def calculate_call_data_cost(
    data: str,
    gtx_data_non_zero: int,
    gtx_data_zero: int,
) -> int:
    zero_bytes, non_zero_bytes = calculate_zero_non_zero_bytes_from_data(data)
    return zero_bytes * gtx_data_zero + non_zero_bytes * gtx_data_non_zero


def estimate_gas_without_call_data(
    txn: GSNTransaction,
    gtx_data_non_zero: int,
    gtx_data_zero: int,
) -> str:
    original_cost = int(txn['gas'], 16)
    call_data_cost = calculate_call_data_cost(
        txn['data'],
        gtx_data_non_zero,
        gtx_data_zero,
    )
    return hex(original_cost - call_data_cost)


def sign_typed_data(domain: EIP721DomainType, types: Dict, message: Dict, primary_type: str, private_key: str) -> str:
    data = {
        'domain': domain,
        'types': types,
        'message': message,
        'primaryType': primary_type,
    }
    signed_message = Web3().eth.account.sign_message(
        encode_structured_data(data),
        private_key=private_key,
    )
    return signed_message.signature.hex()


def sign_relay_request(request: RelayRequest, domain_separator: str, chain_id: int, account: Account) -> str:
    cloned_request = request.copy()
    cloned_request['request']['value'] = int(cloned_request['request']['value'])
    cloned_request['request']['gas'] = int(cloned_request['request']['gas'])
    cloned_request['request']['nonce'] = int(cloned_request['request']['nonce'])
    cloned_request['request']['data'] = bytes.fromhex(cloned_request['request']['data'][2:])
    cloned_request['request']['validUntilTime'] = int(cloned_request['request']['validUntilTime'])
    cloned_request['relayData']['maxFeePerGas'] = int(cloned_request['relayData']['maxFeePerGas'])
    cloned_request['relayData']['maxPriorityFeePerGas'] = int(
        cloned_request['relayData']['maxPriorityFeePerGas'],
    )
    cloned_request['relayData']['transactionCalldataGasUsed'] = int(
        cloned_request['relayData']['transactionCalldataGasUsed'],
    )
    cloned_request['relayData']['paymasterData'] = bytes.fromhex(
        cloned_request['relayData']['paymasterData'][2:],
    )
    cloned_request['relayData']['clientId'] = int(cloned_request['relayData']['clientId'])

    domain = {
        'chainId': int(chain_id),
        'name': domain_separator,
        'verifyingContract': cloned_request['relayData']['forwarder'],
        'version': DOMAIN_SEPARATOR_VERSION,
    }
    types = {
        'EIP712Domain': EIP712TYPE,
        'RelayRequest': RELAY_REQUEST_SIGNED_TYPE,
        'RelayData': RELAY_DATA_SIGNED_TYPE,
    }
    message = {
        **cloned_request['request'],
        'relayData': cloned_request['relayData'],
    }
    return sign_typed_data(domain, types, message, 'RelayRequest', account.private_key)
