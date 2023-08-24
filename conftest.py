import pytest
import os

from py_rally.custom_types import Account, GSNTransaction, RelayRequest
from py_rally.config import NetworkConfig, GSNConfig
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware
import eth_account


@pytest.fixture()
def call_data():
    return {
        'value': '0x3593564c000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000'
        '000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000064e60a'
        'df00000000000000000000000000000000000000000000000000000000000000030a080c0000000000000000000000000000'
        '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000'
        '0000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000'
        '00000000000000000001e0000000000000000000000000000000000000000000000000000000000000030000000000000000'
        '000000000000000000000000000000000000000000000001600000000000000000000000000e9cc0f7e550bd43bd2af22145'
        '63c47699f96479000000000000000000000000ffffffffffffffffffffffffffffffffffffffff00000000000000000000000'
        '000000000000000000000000000000000650d90df000000000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000003fc91a3afd70395cd496c647d5a6cc9d4b2b7fad000000000000000000000000000000000'
        '0000000000000000000000064e60ae700000000000000000000000000000000000000000000000000000000000000e0000000'
        '0000000000000000000000000000000000000000000000000000000041d4ef4bf6632b6ca973be1a07b5ac02d8da34020f53e'
        '5bfd8b440ec2a848c3dff6a26ada3ad3348302fe55150dc112a64a88f4ee2c0fdab9f5afec6d6517a27651c00000000000000'
        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        '00000000100000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000'
        '000000000000000000fc2d09342c9b9cb7005d000000000000000000000000000000000000000000000000016d1ba6fa240f5'
        '400000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000000000000000'
        '00000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000'
        '0000000000000000e9cc0f7e550bd43bd2af2214563c47699f96479000000000000000000000000c02aaa39b223fe8d0a0e5c'
        '4f27ead9083c756cc200000000000000000000000000000000000000000000000000000000000000400000000000000000000'
        '000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000016d1ba6'
        'fa240f54',
        'zero_bytes': 832,
        'non_zero_bytes': 228,
        'zero_cost': 1,
        'non_zero_cost': 2,
        'cost': 1288,
    }


@pytest.fixture()
def txn() -> GSNTransaction:
    return {
        'from_address': '0x39ff33A6959e9EeAc070Fa1b317A4489162897AD',
        'to': '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD',
        'data': '0x0a080c',
        'value': 0,
        'gas': hex(10000),
        'max_fee_per_gas': '1',
        'max_priority_fee_per_gas': '2',
        'paymaster_data': '0x',
        'client_id': 1,
    }


@pytest.fixture()
def relay_request() -> RelayRequest:
    return {
        'request': {
            'from': '0x95d372A4DC5d53C9178695157c69Bf9A9CB91487',
            'to': '0x95d372A4DC5d53C9178695157c69Bf9A9CB91487',
            'value': '0',
            'gas': '0',
            'nonce': '0',
            'data': '0x',
            'validUntilTime': '0',
        },
        'relayData': {
            'maxFeePerGas': '0',
            'maxPriorityFeePerGas': '0',
            'transactionCalldataGasUsed': '0',
            'relayWorker': '0x579de7c56cd9a07330504a7c734023a9f703778a',
            'paymaster': '0x579de7c56cd9a07330504a7c734023a9f703778a',
            'forwarder': '0x579de7c56cd9a07330504a7c734023a9f703778a',
            'paymasterData': '0x',
            'clientId': '1',
        },
    }


@pytest.fixture()
def signature_account() -> Account:
    return Account(
        '0x18d17d375047503d4b3127a61d0ac6a37a22a3e5a11a612f853e5c5eadc37235',
        '0x95d372A4DC5d53C9178695157c69Bf9A9CB91487'
    )


@pytest.fixture()
def client_account() -> Account:
    account = eth_account.Account.create()
    return Account(
        account.key.hex(),
        account.address,
    )


@pytest.fixture(scope='module')
def test_config() -> NetworkConfig:
    gsn_config = GSNConfig(
        paymaster_address='0x8b3a505413Ca3B0A17F077e507aF8E3b3ad4Ce4d',
        forwarder_address='0xB2b5841DBeF766d4b521221732F9B618fCf34A87',
        relay_hub_address='0x3232f21A6E08312654270c78A773f00dd61d60f5',
        relay_worker_address='0xb9950b71ec94cbb274aeb1be98e697678077a17f',
        relay_url='https://api.rallyprotocol.com',
        rpc_url=os.getenv('MUMBAI_RPC_URL'),
        chain_id=80001,
        max_acceptance_budget=285252,
        domain_separator_name='GSN Relayed Transaction',
        gtx_data_zero=16,
        gtx_data_non_zero=4,
        request_valid_seconds=172800,
        max_paymaster_data_length=300,
        max_approval_data_length=300,
        max_relay_nonce_gap=3,
    )

    network_config = NetworkConfig(
        contracts={
            'rly_erc20': '0x1C7312Cb60b40cF586e796FEdD60Cf243286c9E9',
            'faucet': '0xe7C3BD692C77Ec0C0bde523455B9D142c49720fF',
        },
        gsn_config=gsn_config,
        web3=Web3(HTTPProvider(gsn_config.rpc_url)),
        relayer_api_key=os.getenv('RLY_API_KEY'),
    )
    network_config.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return network_config
