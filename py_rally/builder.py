from py_rally.config import GSNConfig, NetworkConfig
from py_rally.network import RallyNetworkClient
from py_rally.gsn import RallyGSNClient
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware


class NetworkClientBuilder:
    @staticmethod
    def build(
            paymaster: str,
            forwarder: str,
            relay_hub: str,
            relay_worker: str,
            rpc_url: str,
            chain_id: int,
            max_acceptance_budget: int,
            domain_separator: str,
            gtx_data_zero: int,
            gtx_data_non_zero: int,
            request_valid_secs: int,
            max_paymaster_data_len: int,
            max_approval_data_len: int,
            max_relay_nonce_gap: int,
            relayer_api_key: str
    ):
        gsn_config = GSNConfig(
            paymaster_address=paymaster,
            forwarder_address=forwarder,
            relay_hub_address=relay_hub,
            relay_worker_address=relay_worker,
            relay_url='https://api.rallyprotocol.com',
            rpc_url=rpc_url,
            chain_id=chain_id,
            max_acceptance_budget=max_acceptance_budget,
            domain_separator_name=domain_separator,
            gtx_data_zero=gtx_data_zero,
            gtx_data_non_zero=gtx_data_non_zero,
            request_valid_seconds=request_valid_secs,
            max_paymaster_data_length=max_paymaster_data_len,
            max_approval_data_length=max_approval_data_len,
            max_relay_nonce_gap=max_relay_nonce_gap,
        )
        network_config = NetworkConfig(
            contracts={
                'rly_erc20': '0x1C7312Cb60b40cF586e796FEdD60Cf243286c9E9',
                'faucet': '0x78a0794Bb3BB06238ed5f8D926419bD8fc9546d8',
            },
            gsn_config=gsn_config,
            web3=Web3(HTTPProvider(gsn_config.rpc_url)),
            relayer_api_key=relayer_api_key,
        )
        if chain_id == 80001:
            network_config.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        gsn_client = RallyGSNClient(network_config)
        return RallyNetworkClient(gsn_client)

    @classmethod
    def get_rally_mumbai_client(cls):
        client = cls.build(
            '0x8b3a505413Ca3B0A17F077e507aF8E3b3ad4Ce4d',
            '0xB2b5841DBeF766d4b521221732F9B618fCf34A87',
            '0x3232f21A6E08312654270c78A773f00dd61d60f5',
            '0xb9950b71ec94cbb274aeb1be98e697678077a17f',
            'https://polygon-mumbai.g.alchemy.com/v2/-dYNjZXvre3GC9kYtwDzzX4N8tcgomU4',
            8001,
            285252,
            'GSN Relayed Transaction',
            4,
            16,
            172800,
            300,
            300,
            3,
            ''
        )
        client.gsn_client.config.contracts['rly_erc20'] = '0x1C7312Cb60b40cF586e796FEdD60Cf243286c9E9'
        client.gsn_client.config.contracts['faucet'] = '0xe7C3BD692C77Ec0C0bde523455B9D142c49720fF'
        return client

    @classmethod
    def get_rally_polygon_client(cls):
        client = cls.build(
            '0x29CAa31142D17545C310437825aA4C53FbE621C3',
            '0xB2b5841DBeF766d4b521221732F9B618fCf34A87',
            '0xfCEE9036EDc85cD5c12A9De6b267c4672Eb4bA1B',
            '0x579de7c56cd9a07330504a7c734023a9f703778a',
            'https://polygon-mainnet.g.alchemy.com/v2/-dYNjZXvre3GC9kYtwDzzX4N8tcgomU4',
            137,
            285252,
            'GSN Relayed Transaction',
            4,
            16,
            172800,
            300,
            0,
            3,
            ''
        )
        client.gsn_client.config.contracts['rly_erc20'] = '0x76b8D57e5ac6afAc5D415a054453d1DD2c3C0094'
        client.gsn_client.config.contracts['faucet'] = '0x78a0794Bb3BB06238ed5f8D926419bD8fc9546d8'
        return client
