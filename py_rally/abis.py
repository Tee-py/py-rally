import json

FORWARDER_ABI = json.load(open('py_rally/ABI/IForwarder.json'))
RELAY_HUB_ABI = json.load(open('py_rally/ABI/IRelayHub.json'))
TOKEN_FAUCET_ABI = json.load(open('py_rally/ABI/tokenFaucetData.json'))['abi']
ERC20_ABI = json.load(open("py_rally/ABI/IERC20.json"))
