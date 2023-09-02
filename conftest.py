import os

import eth_account
import pytest

from py_rally import NetworkClientBuilder
from py_rally.custom_types import Account, GSNTransaction, RelayRequest


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
        os.getenv('PRIVATE_KEY'),
        '0x95d372A4DC5d53C9178695157c69Bf9A9CB91487',
    )


@pytest.fixture
def client_account() -> Account:
    account = eth_account.Account.create()
    return Account(
        account.key.hex(),
        account.address,
    )


@pytest.fixture(scope='module')
def polygon_client():
    return NetworkClientBuilder.get_rally_polygon_client()


@pytest.fixture(scope='module')
def mumbai_client():
    return NetworkClientBuilder.get_rally_mumbai_client()
