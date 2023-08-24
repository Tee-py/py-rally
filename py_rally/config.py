from dataclasses import dataclass
from typing import Optional

from web3 import Web3

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
