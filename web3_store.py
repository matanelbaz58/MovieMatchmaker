from web3 import Web3
import json
import utils
# Connect to Sepolia testnet
sepolia_url = 'https://sepolia.infura.io/v3/a32106b340fb4f1aa81105e66a70b2ff'
w3 = Web3(Web3.HTTPProvider(sepolia_url))

# Ensure connection is successful
if w3.is_connected():
    print("Connected to Sepolia Testnet")
else:
    print("Failed to connect to Sepolia Testnet\n\n\n")

# Your contract details
contract_address = '0x158ca7e48d81031f9fF65425b4B084ECd1853107'
contract_abi = json.loads(utils.ABI)  # Replace YOUR_CONTRACT_ABI with the actual ABI json string

# Initialize contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Example of reading from the contract (a public variable or a function that doesn't change state)
# Replace 'example_read_function' with your actual function name
read_result = contract.functions.retrive().call()
print(f"Read Result: {read_result}")
print("\n\n\n---------------------------------------------------\n\n\n")
# Example of writing to the contract (requires a transaction)
# Replace 'example_write_function' and 'FUNCTION_ARGUMENTS' with your actual function and arguments
tx_function = contract.functions.store (0x6057361d)(121234)
wallet_address = '0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B'
wallet_private_key = '7adf8381908aee6ee141616efb1f74a5f76278f66a1a83b1178e364db0d3969a'

# Estimate gas for the transaction
gas_estimate = tx_function.estimate_gas({'from': wallet_address})

# Get current nonce for the wallet
nonce = w3.eth.get_transaction_count(wallet_address)# Create transaction dictionary
tx = tx_function.build_transaction({
    'chainId': w3.eth.chain_id,
    'gas': gas_estimate,
    'nonce': nonce,
})

# Sign the transaction
signed_tx = w3.eth.account.sign_transaction(tx, wallet_private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt (optional, for confirmation)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")
