import os
import json
from web3 import Web3
from django.conf import settings


# Deployed smart contract address
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS


# Load ABI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "abi.json"), "r") as f:
    CONTRACT_ABI = json.load(f)


# Connect to Ethereum Sepolia
w3 = Web3(Web3.HTTPProvider(settings.SEPOLIA_RPC_URL))


# Create contract instance
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=CONTRACT_ABI
)

# Backend wallet
PRIVATE_KEY = settings.PRIVATE_KEY
ACCOUNT = w3.eth.account.from_key(PRIVATE_KEY)