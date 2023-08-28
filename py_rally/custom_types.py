from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypedDict


class EIP721DomainType(TypedDict):
    chainId: int
    name: str
    verifyingContract: str
    version: str


class MetaTxMethod(Enum):
    Permit = 'permit'
    ExecuteMetaTransaction = 'executeMetaTransaction'

    @classmethod
    def from_method_str(cls, value: str):
        return cls(value)


class EIP721MessageType(TypedDict):
    name: str
    type: str


class ConfigContracts(TypedDict):
    faucet: str
    rly_erc20: str


class GSNTransaction(TypedDict):
    from_address: str
    to: str
    data: str
    value: int
    # Hex string
    gas: Optional[str]
    # Hex string
    max_fee_per_gas: str
    # Hex string
    max_priority_fee_per_gas: str
    paymaster_data: str
    client_id: int


class GSNServerConfigResponse(TypedDict):
    relayWorkerAddress: str
    relayManagerAddress: str
    relayHubAddress: str
    ownerAddress: str
    minMaxPriorityFeePerGas: str
    maxMaxFeePerGas: str
    minMaxFeePerGas: str
    maxAcceptanceBudget: str
    chainId: str
    networkId: str
    ready: bool
    version: str


ForwarderRequest = TypedDict(
    'ForwarderRequest',
    {
        'from': str,
        'to': str,
        'value': str,
        'gas': str,
        'nonce': str,
        'data': str,
        'validUntilTime': str,
    },
)


class RelayHttpRequestMetadata(TypedDict):
    maxAcceptanceBudget: str
    relayHubAddress: str
    signature: str
    approvalData: str
    relayMaxNonce: int
    relayLastKnownNonce: int
    domainSeparatorName: str
    relayRequestId: str


class RelayData(TypedDict):
    maxFeePerGas: str
    maxPriorityFeePerGas: str
    transactionCalldataGasUsed: str
    relayWorker: str
    paymaster: str
    paymasterData: str
    clientId: str
    forwarder: str


class RelayRequest(TypedDict):
    request: ForwarderRequest
    relayData: RelayData


class RelayHttpRequest(TypedDict):
    relayRequest: RelayRequest
    metadata: RelayHttpRequestMetadata


@dataclass(frozen=True)
class Account:
    private_key: str
    address: str
