import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FORWARDER_ABI_FILE = BASE_DIR / 'ABI' / 'IForwarder.json'
RELAY_HUB_ABI_FILE = BASE_DIR / 'ABI' / 'IRelayHub.json'
TOKEN_FAUCET_ABI_FILE = BASE_DIR / 'ABI' / 'tokenFaucetData.json'
ERC20_ABI_FILE = BASE_DIR / 'ABI' / 'IERC20.json'
FORWARDER_ABI = []
RELAY_HUB_ABI = []
TOKEN_FAUCET_ABI = []
ERC20_ABI = []

with FORWARDER_ABI_FILE.open('r') as f:
    FORWARDER_ABI = json.load(f)

with RELAY_HUB_ABI_FILE.open('r') as f:
    RELAY_HUB_ABI = json.load(f)

with TOKEN_FAUCET_ABI_FILE.open('r') as f:
    TOKEN_FAUCET_ABI = json.load(f)['abi']

with ERC20_ABI_FILE.open('r') as f:
    ERC20_ABI = json.load(f)
