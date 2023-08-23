from dataclasses import dataclass
from typing import Optional

from web3 import HTTPProvider, Web3

from py_rally.custom_types import ConfigContracts


@dataclass
class GSNConfig:
    paymaster_address: str
    forwarder_address: str
    relay_hub_address: str
    relay_worker_address: str
    relay_url: str
    rpc_url: str
    chain_id: int
    max_acceptance_budget: int
    domain_separator_name: str
    gtx_data_zero: int
    gtx_data_non_zero: int
    request_valid_seconds: int
    max_paymaster_data_length: int
    max_approval_data_length: int
    max_relay_nonce_gap: int


@dataclass
class NetworkConfig:
    contracts: ConfigContracts
    relayer_api_key: Optional[str]
    gsn_config: GSNConfig
    web3: Web3


polygon_gsn_config: GSNConfig = GSNConfig(
    paymaster_address='0x29CAa31142D17545C310437825aA4C53FbE621C3',
    forwarder_address='0xB2b5841DBeF766d4b521221732F9B618fCf34A87',
    relay_hub_address='0xfCEE9036EDc85cD5c12A9De6b267c4672Eb4bA1B',
    relay_worker_address='0x579de7c56cd9a07330504a7c734023a9f703778a',
    relay_url='https://api.rallyprotocol.com',
    rpc_url='https://polygon-mainnet.g.alchemy.com/v2/-dYNjZXvre3GC9kYtwDzzX4N8tcgomU4',
    chain_id=137,
    max_acceptance_budget=285252,
    domain_separator_name='GSN Relayed Transaction',
    gtx_data_zero=16,
    gtx_data_non_zero=4,
    request_valid_seconds=172800,
    max_paymaster_data_length=300,
    max_approval_data_length=0,
    max_relay_nonce_gap=3,
)

PolygonNetworkConfig: NetworkConfig = NetworkConfig(
    contracts={
        'rly_erc20': '0x76b8D57e5ac6afAc5D415a054453d1DD2c3C0094',
        'faucet': '0x78a0794Bb3BB06238ed5f8D926419bD8fc9546d8',
    },
    gsn_config=polygon_gsn_config,
    web3=Web3(HTTPProvider(polygon_gsn_config.rpc_url)),
    relayer_api_key=None,
)
