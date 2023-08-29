from unittest.mock import MagicMock, patch

from py_rally.custom_types import Account, MetaTxMethod
from py_rally.network import RallyNetworkClient


@patch('requests.post')
def test_mumbai_network_client(mock_requests, signature_account: Account, mumbai_client: RallyNetworkClient):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        'signedTx': '0x02f905f68301388182075e84ba574ed284ba574ed2830768e3943232f21a6e08312654270c78a773f00dd61d60f580b9'
        '05846ca862e200000000000000000000000000000000000000000000000000000000000000a00000000000000000000000'
        '000000000000000000000000000000000000045a4400000000000000000000000000000000000000000000000000000000'
        '000000e0000000000000000000000000000000000000000000000000000000000000048000000000000000000000000000'
        '00000000000000000000000000000000000500000000000000000000000000000000000000000000000000000000000000'
        '001747534e2052656c61796564205472616e73616374696f6e000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000280'
        '00000000000000000000000095d372a4dc5d53c9178695157c69bf9a9cb914870000000000000000000000001c7312cb60'
        'b40cf586e796fedd60cf243286c9e900000000000000000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000000000000000000000000000d98000000000000000000000000000000000000000'
        '0000000000000000000000000300000000000000000000000000000000000000000000000000000000000000e000000000'
        '00000000000000000000000000000000000000000000000064efcdbe000000000000000000000000000000000000000000'
        '00000000000000000001240c53c51c00000000000000000000000095d372a4dc5d53c9178695157c69bf9a9cb914870000'
        '0000000000000000000000000000000000000000000000000000000000a0ed3c6a4ae87006622586ff13083545c043fd5f'
        '3e325283314f251380984a05116b8bbe3f72e08ff3aad91e9b34c837097bd02334a8e1dcd954a02e4c7da74b8f00000000'
        '0000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000'
        '0000000000000000000044a9059cbb00000000000000000000000057c6e736fc7e6ef96b7812ffc8af6cfc8cde028f0000'
        '000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000'
        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000ba574ed200000000000000000000000000000000000000000000000000000000ba'
        '574ed20000000000000000000000000000000000000000000000000000000000004d34000000000000000000000000b995'
        '0b71ec94cbb274aeb1be98e697678077a17f0000000000000000000000008b3a505413ca3b0a17f077e507af8e3b3ad4ce'
        '4d000000000000000000000000b2b5841dbef766d4b521221732f9b618fcf34a8700000000000000000000000000000000'
        '00000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000100'
        '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000419b0bfa0e867074dcaf7f5395b2a5b9786955bd1c3a8645fc78f4c9873eebeb2b53c79f'
        '2dc8e594cda025de8b34fa3610a708754ec382940053470791d4fa3f001c00000000000000000000000000000000000000'
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000004165f07da87c'
        '0f0afeff57765243ac74d6ddaa27396c3a3365e24cef774ebcfd5c5bfddaaee49f19b1cae62165acabe2b0f9b04c3d61c2'
        '31cd3b4758ff748472121b00000000000000000000000000000000000000000000000000000000000000c001a03bd4e067'
        '09e991ee2f85dadbdbdbffa9e786f1e9fe9e6728f896eb139d463b52a04c55cc828b02d924d37f684fca6c79e8fbe6813a'
        '4b2d4656a3365633a4558c25',
        'nonceGapFilled': {},
    }
    mock_requests.return_value = mock_response
    # mumbai_client.token_transfer(
    #     signature_account,
    #     '0x57c6E736FC7e6Ef96b7812FFc8AF6cFC8cdE028f',
    #     10,
    #     '0x001B3B4d0F3714Ca98ba10F6042DaEbF0B1B7b6F',
    #     MetaTxMethod.Permit
    mumbai_client.token_transfer(
        signature_account,
        '0x57c6E736FC7e6Ef96b7812FFc8AF6cFC8cdE028f',
        1,
        mumbai_client.gsn_client.config.contracts['rly_erc20'],
        MetaTxMethod.ExecuteMetaTransaction,
    )


# @patch('requests.post')
# def test_polygon_network_client(signature_account: Account, polygon_client):
# mock_response.json.return_value = {
#     '05846ca862e200000000000000000000000000000000000000000000000000000000000000a00000000000000000000000'
#     '000000000000000000000000000000000000045a4400000000000000000000000000000000000000000000000000000000'
#     '000000e0000000000000000000000000000000000000000000000000000000000000048000000000000000000000000000'
#     '00000000000000000000000000000000000500000000000000000000000000000000000000000000000000000000000000'
#     '001747534e2052656c61796564205472616e73616374696f6e000000000000000000000000000000000000000000000000'
#     '00000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000280'
#     '00000000000000000000000095d372a4dc5d53c9178695157c69bf9a9cb914870000000000000000000000001c7312cb60'
#     'b40cf586e796fedd60cf243286c9e900000000000000000000000000000000000000000000000000000000000000000000'
#     '00000000000000000000000000000000000000000000000000000000d98000000000000000000000000000000000000000'
#     '0000000000000000000000000300000000000000000000000000000000000000000000000000000000000000e000000000'
#     '00000000000000000000000000000000000000000000000064efcdbe000000000000000000000000000000000000000000'
#     '00000000000000000001240c53c51c00000000000000000000000095d372a4dc5d53c9178695157c69bf9a9cb914870000'
#     '0000000000000000000000000000000000000000000000000000000000a0ed3c6a4ae87006622586ff13083545c043fd5f'
#     '3e325283314f251380984a05116b8bbe3f72e08ff3aad91e9b34c837097bd02334a8e1dcd954a02e4c7da74b8f00000000'
#     '0000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000'
#     '0000000000000000000044a9059cbb00000000000000000000000057c6e736fc7e6ef96b7812ffc8af6cfc8cde028f0000'
#     '000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000'
#     '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
#     '00000000000000000000000000000000ba574ed200000000000000000000000000000000000000000000000000000000ba'
#     '574ed20000000000000000000000000000000000000000000000000000000000004d34000000000000000000000000b995'
#     '0b71ec94cbb274aeb1be98e697678077a17f0000000000000000000000008b3a505413ca3b0a17f077e507af8e3b3ad4ce'
#     '4d000000000000000000000000b2b5841dbef766d4b521221732f9b618fcf34a8700000000000000000000000000000000'
#     '00000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000100'
#     '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
#     '00000000000000000000000000419b0bfa0e867074dcaf7f5395b2a5b9786955bd1c3a8645fc78f4c9873eebeb2b53c79f'
#     '2dc8e594cda025de8b34fa3610a708754ec382940053470791d4fa3f001c00000000000000000000000000000000000000'
#     '000000000000000000000000000000000000000000000000000000000000000000000000000000000000004165f07da87c'
#     '0f0afeff57765243ac74d6ddaa27396c3a3365e24cef774ebcfd5c5bfddaaee49f19b1cae62165acabe2b0f9b04c3d61c2'
#     '31cd3b4758ff748472121b00000000000000000000000000000000000000000000000000000000000000c001a03bd4e067'
#     '09e991ee2f85dadbdbdbffa9e786f1e9fe9e6728f896eb139d463b52a04c55cc828b02d924d37f684fca6c79e8fbe6813a'
#     '4b2d4656a3365633a4558c25',
# network_client.token_transfer(
#     signature_account,
#     '0x57c6E736FC7e6Ef96b7812FFc8AF6cFC8cdE028f',
#     10,
#     '0x001B3B4d0F3714Ca98ba10F6042DaEbF0B1B7b6F',
#     MetaTxMethod.Permit
# polygon_client.token_transfer(
#     signature_account,
#     '0x57c6E736FC7e6Ef96b7812FFc8AF6cFC8cdE028f',
#     1,
#     '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
#     MetaTxMethod.Permit,
