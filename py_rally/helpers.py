import copy

from eth_account.messages import encode_structured_data
from web3 import Web3
from web3.exceptions import ContractLogicError

from py_rally.abis import ERC20_ABI
from py_rally.constants import (
    DOMAIN_SEPARATOR_VERSION,
    EIP712_SALT_TYPE,
    EIP712TYPE,
    HASH_ZERO,
    RELAY_DATA_SIGNED_TYPE,
    RELAY_REQUEST_SIGNED_TYPE,
)
from py_rally.custom_types import Account, EIP721DomainType, GSNTransaction, RelayRequest


def calculate_zero_non_zero_bytes_from_data(data: str) -> tuple[int, int]:
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


def sign_typed_data(domain: EIP721DomainType, types: dict, message: dict, primary_type: str, private_key: str) -> str:
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
    cloned_request: dict = copy.deepcopy(request)
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


def get_erc20_token(web3: Web3, token_address: str):
    return web3.eth.contract(web3.to_checksum_address(token_address), abi=ERC20_ABI)


def get_token_balance(web3: Web3, token_address: str, account: Account):
    token_contract = get_erc20_token(web3, token_address)
    balance = token_contract.functions.balanceOf(account.address).call()
    decimals = token_contract.functions.decimals().call()
    return balance / 10**decimals


def get_meta_txn_eip712_signature(account: Account, name: str, contract: str, data: str, nonce: int, chain_id: str):
    salt = '0x00' + f'{int(chain_id):#0{64}x}'[2:]
    types = {
        'EIP712Domain': EIP712_SALT_TYPE,
        'MetaTransaction': [
            {'name': 'nonce', 'type': 'uint256'},
            {'name': 'from', 'type': 'address'},
            {'name': 'functionSignature', 'type': 'bytes'},
        ],
    }
    domain = {'name': name, 'version': '1', 'verifyingContract': contract, 'salt': bytes.fromhex(salt[2:])}
    message = {
        'from': account.address,
        'functionSignature': bytes.fromhex(data[2:]),
        'nonce': nonce,
    }
    eip712_data = {
        'domain': domain,
        'message': message,
        'primaryType': 'MetaTransaction',
        'types': types,
    }
    return Web3().eth.account.sign_message(
        encode_structured_data(eip712_data),
        private_key=account.private_key,
    )


def get_permit_eip712_signature(
    account: Account,
    spender: str,
    decimal_amount: int,
    name: str,
    contract: str,
    nonce: int,
    deadline: int,
    salt: str,
    chain_id: int,
):
    types = {
        'EIP712Domain': EIP712_SALT_TYPE,
        'Permit': [
            {'name': 'owner', 'type': 'address'},
            {'name': 'spender', 'type': 'address'},
            {'name': 'value', 'type': 'uint256'},
            {'name': 'nonce', 'type': 'uint256'},
            {'name': 'deadline', 'type': 'uint256'},
        ],
    }
    domain = {'name': name, 'version': '1', 'chainId': chain_id, 'verifyingContract': contract}
    if salt != HASH_ZERO:
        domain['salt'] = salt
    message = {
        'owner': account.address,
        'spender': spender,
        'value': str(decimal_amount),
        'nonce': nonce,
        'deadline': deadline,
    }
    eip712_data = {
        'domain': domain,
        'message': message,
        'primaryType': 'MetaTransaction',
        'types': types,
    }
    return Web3().eth.account.sign_message(
        encode_structured_data(eip712_data),
        private_key=account.private_key,
    )


def tx_to_gsn_txn(tx: dict) -> GSNTransaction:
    return {
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


# def get_eip712_domain_for_permit(token_contract):


def get_permit_txn(
    web3: Web3,
    account: Account,
    paymaster_address: str,
    to: str,
    amount: float,
    contract: str,
    chain_id: int,
) -> GSNTransaction:
    token_contract = get_erc20_token(web3, contract)
    name = token_contract.functions.name().call()
    nonce = token_contract.functions.nonces(account.address).call()
    decimals = token_contract.functions.decimals().call()
    eip712_domain = token_contract.functions.eip712Domain().call()
    salt = eip712_domain['salt']
    latest_block = web3.eth.get_block('latest')
    deadline = latest_block['timestamp'] + 45
    decimal_amount = amount * 10**decimals
    signed_message = get_permit_eip712_signature(
        account,
        paymaster_address,
        decimal_amount,
        name,
        contract,
        nonce,
        deadline,
        salt,
        chain_id,
    )
    r_value = signed_message.r
    s_value = signed_message.s
    v_value = signed_message.v
    permit_tx = token_contract.functions.permit(
        account.address,
        paymaster_address,
        decimal_amount,
        deadline,
        v_value,
        bytes.fromhex(hex(r_value)[2:]),
        bytes.fromhex(hex(s_value)[2:]),
    ).build_transaction({'from': account.address})
    transfer_from_tx = token_contract.functions.transferFrom(
        account.address,
        to,
        decimal_amount,
    ).build_transaction()
    paymaster_data = '0x' + contract.replace('0x', '') + transfer_from_tx['data'].replace('0x', '')
    gsn_tx = tx_to_gsn_txn(permit_tx)
    gsn_tx['paymaster_data'] = paymaster_data
    return gsn_tx


def get_execute_meta_transaction_txn(
    web3: Web3,
    account: Account,
    to: str,
    amount: float,
    contract: str,
    chain_id: str,
) -> GSNTransaction:
    token_contract = get_erc20_token(web3, contract)
    name = token_contract.functions.name().call()
    try:
        nonce = token_contract.functions.getNonce(account.address).call()
    except ContractLogicError:
        nonce = token_contract.functions.nonces(account.address).call()
    decimals = token_contract.functions.decimals().call()
    decimal_amount = int(amount * 10**decimals)

    transfer_data = token_contract.encodeABI('transfer', [to, decimal_amount])

    signature = get_meta_txn_eip712_signature(account, name, contract, transfer_data, nonce, chain_id)
    r_value = signature.r
    s_value = signature.s
    v_value = signature.v
    tx = token_contract.functions.executeMetaTransaction(
        account.address,
        bytes.fromhex(transfer_data[2:]),
        bytes.fromhex(hex(r_value)[2:]),
        bytes.fromhex(hex(s_value)[2:]),
        v_value,
    ).build_transaction({'from': account.address})
    return tx_to_gsn_txn(tx)
