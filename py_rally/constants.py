EIP712TYPE = [
    {'name': 'name', 'type': 'string'},
    {'name': 'version', 'type': 'string'},
    {'name': 'chainId', 'type': 'uint256'},
    {'name': 'verifyingContract', 'type': 'address'},
]
EIP712_SALT_TYPE = [
    {'name': 'name', 'type': 'string'},
    {'name': 'version', 'type': 'string'},
    {'name': 'verifyingContract', 'type': 'address'},
    {'name': 'salt', 'type': 'bytes32'}
]
FORWARDER_DATA_SIGNED_TYPE = [
    {'name': 'from', 'type': 'address'},
    {'name': 'to', 'type': 'address'},
    {'name': 'value', 'type': 'uint256'},
    {'name': 'gas', 'type': 'uint256'},
    {'name': 'nonce', 'type': 'uint256'},
    {'name': 'data', 'type': 'bytes'},
    {'name': 'validUntilTime', 'type': 'uint256'},
]
RELAY_DATA_SIGNED_TYPE = [
    {'name': 'maxFeePerGas', 'type': 'uint256'},
    {'name': 'maxPriorityFeePerGas', 'type': 'uint256'},
    {'name': 'transactionCalldataGasUsed', 'type': 'uint256'},
    {'name': 'relayWorker', 'type': 'address'},
    {'name': 'paymaster', 'type': 'address'},
    {'name': 'forwarder', 'type': 'address'},
    {'name': 'paymasterData', 'type': 'bytes'},
    {'name': 'clientId', 'type': 'uint256'},
]
RELAY_REQUEST_SIGNED_TYPE = [
    *FORWARDER_DATA_SIGNED_TYPE,
    {'name': 'relayData', 'type': 'RelayData'},
]
DOMAIN_SEPARATOR_VERSION = '3'
OK_RESPONSE = 200
