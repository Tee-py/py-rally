# PyRally
Welcome to the **Rally Protocol Python SDK!** This SDK provides an easy way to interact with 
the Rally Protocol gas station network. 
With this SDK, you can easily submit gasless transactions to the Rally GSN API. For more information about
gasless transactions and the Rally Protocol, visit [Rally Protocol](https://docs.rallyprotocol.com/rally-mobile-sdk/sponsored-gasless-transactions/overview)

# Installation
```shell
pip install py_rally
```

# Usage
Navigate to [Rally App](https://app.rallyprotocol.com/) to generate API Keys for polygon mumbai and polygon pos.

## Getting started with the RallyNetworkClient
The network client allows you to send transactions to the relayer and also transfer supported tokens from one address to another.
The SDK provides both mumbai and polygon POS network clients.
 ```python
from py_rally import NetworkClientBuilder
from py_rally.custom_types import Account, MetaTxMethod

# Create an Account Object
account = Account('<PRIVATE_KEY>', '<ADDRESS>')

# Get polygon mumbai testnet client
mumbai_network_client = NetworkClientBuilder.get_rally_mumbai_client()
mumbai_network_client.set_api_key('<RALLY MUMBAI API KEY>')

# Get polygon mainnet client
polygon_network_client = NetworkClientBuilder.get_rally_polygon_client()
polygon_network_client.set_api_key('<RALLY MAINNET API KEY>')

# Claim Rally into account on testnet
mumbai_network_client.claim_rally(account)

# Transfer rally to another account on testnet
mumbai_network_client.token_transfer(
    account,
    '<TO ADDRESS>',
    1,
    '<RALLY TESTNET TOKEN ADDRESS>',
    MetaTxMethod.ExecuteMetaTransaction
) # Rally Token supports execute meta transaction.
```

## Calling contracts not supported by the SDK
The SDK allows sending transactions to the relayer API for contracts not supported by the SDK.
The contract has to be a supported contract on Rally Protocol. Rally Protocol supports `ERC2771 compatible contracts`. For more
information about this, visit [Rally documentation](https://docs.rallyprotocol.com/rally-mobile-sdk/sponsored-gasless-transactions/get-started#supported-contracts)
```python
from py_rally import NetworkClientBuilder
from py_rally.custom_types import Account

client = NetworkClientBuilder.get_rally_polygon_client()
client.set_api_key('<API KEY>')

# Build raw transaction using web3.py
signer = Account('<PRIVATE_KEY>', '<ADDRESS>')
ABI = ['CONTRACT ABI']
contract_address = client.web3.to_checksum_address('<Address>')
contract = client.web3.eth.contract(contract_address, abi=ABI)
tx = contract.functions.claim().build_transaction({'from': signer.address})
gsn_txn = {
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
tx_hash = client.relay_transaction(signer, gsn_txn)
```