from py_rally.custom_types import Account, GSNTransaction, RelayRequest
from py_rally.helpers import (
    calculate_call_data_cost,
    calculate_zero_non_zero_bytes_from_data,
    estimate_gas_without_call_data,
    sign_relay_request,
)


def test_calculate_zero_non_zero_bytes_from_data(call_data):
    zero_bytes, non_zero_bytes = calculate_zero_non_zero_bytes_from_data(call_data['value'])
    assert zero_bytes == call_data['zero_bytes']
    assert non_zero_bytes == call_data['non_zero_bytes']


def test_calculate_call_data_cost(call_data):
    cost = calculate_call_data_cost(call_data['value'], call_data['non_zero_cost'], call_data['zero_cost'])
    assert cost == call_data['cost']


def test_estimate_gas_without_call_data(txn: GSNTransaction, call_data):
    txn['data'] = call_data['value']

    cost = estimate_gas_without_call_data(txn, call_data['non_zero_cost'], call_data['zero_cost'])
    assert int(cost, 16) == (int(txn['gas'], 16) - call_data['cost'])


def test_sign_relay_request(relay_request: RelayRequest, account: Account):
    signature = sign_relay_request(relay_request, 'Test', 1, account)
    assert (
        signature == '0xcabf842b2c918efd73e9c82ad3587f8403080edb369e5389ef75071c230a9a9c2a99c2b826e'
        'db72ffea13ddeb0ea1d5525311771ca73bab26b3960e9a06f8f511b'
    )
