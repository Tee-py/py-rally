from unittest.mock import MagicMock, patch

from py_rally import RallyGSNClient
from py_rally.abis import TOKEN_FAUCET_ABI
from py_rally.config import NetworkConfig
from py_rally.custom_types import Account, GSNTransaction


@patch('requests.post')
def test_rally_gsn_client(mock_requests, test_config: NetworkConfig, client_account: Account):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        'signedTx': '0x02f904d6830138818206f184a728f7fd84a728f7fd8307be6f943232f21a6e08312654270c78a773f00dd61d60f580b9'
        '04646ca862e200000000000000000000000000000000000000000000000000000000000000a00000000000000000000000'
        '000000000000000000000000000000000000045a4400000000000000000000000000000000000000000000000000000000'
        '000000e0000000000000000000000000000000000000000000000000000000000000036000000000000000000000000000'
        '000000000000000000000000000000000003e0000000000000000000000000000000000000000000000000000000000000'
        '001747534e2052656c61796564205472616e73616374696f6e000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000160'
        '00000000000000000000000047b6390a09c3f0b911da85838e968110747e5062000000000000000000000000e7c3bd692c'
        '77ec0c0bde523455b9d142c49720ff00000000000000000000000000000000000000000000000000000000000000000000'
        '000000000000000000000000000000000000000000000000000000013fc900000000000000000000000000000000000000'
        '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e000000000'
        '00000000000000000000000000000000000000000000000064ea6454000000000000000000000000000000000000000000'
        '00000000000000000000044e71d92d00000000000000000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000000000000000a728f7fd0000000000000000000000000000000000000000000000'
        '0000000000a728f7fd00000000000000000000000000000000000000000000000000000000000040c80000000000000000'
        '00000000b9950b71ec94cbb274aeb1be98e697678077a17f0000000000000000000000008b3a505413ca3b0a17f077e507'
        'af8e3b3ad4ce4d000000000000000000000000b2b5841dbef766d4b521221732f9b618fcf34a8700000000000000000000'
        '00000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000'
        '00000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000000000418bcc3def9568fd754dae33ad19e5ab8e8c9de123a472ac6157b7f9c59c'
        '75d9261fd0918304bda2ad21248b515482d43e936a66c417dffe848acee097faddb5ca1b00000000000000000000000000'
        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        '41d9652f182b8901f4763c3074fb1c5674bcfaa6d2073564799d6c41b1d9fc751b2ed7a73db416c8a98d2d7cf2af9fb4d5'
        '30cf6f621575dc9ca410ecb1bfcb85cf1b00000000000000000000000000000000000000000000000000000000000000c0'
        '01a0b61dda576a0342d223c92e5488ffeeb043d377c204d9db986ea8c977363af787a05abec4b11fd6ff337e1da8fcac6f'
        '7357bc9a4ea2e636b9fe415bcaf2c1d3adb3',
        'nonceGapFilled': {},
    }
    mock_requests.return_value = mock_response
    gsn_client = RallyGSNClient(test_config)
    token_faucet_address = test_config.web3.to_checksum_address(test_config.contracts['faucet'])
    token_faucet_contract = test_config.web3.eth.contract(token_faucet_address, abi=TOKEN_FAUCET_ABI)
    tx = token_faucet_contract.functions.claim().build_transaction({'from': client_account.address})
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
    tx_hash = gsn_client.submit_transaction(client_account, gsn_txn)
    assert tx_hash == '0x23b0e64773bf41780138a3182b676e8b4b38a92ae59eed4ae9fa8ab3f49fe4bd'
