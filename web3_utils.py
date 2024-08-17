import requests
from web3 import Web3
import json
from eth_account.messages import encode_defunct

SERVER_URL = 'http://localhost:5000'
CONTRACT_ADDRESS = '0xc4311656c7e3164a05fb13a6E395872d4412b78b'
SEPOLIA_API_KEY = 'a32106b340fb4f1aa81105e66a70b2ff' #TODO: is this the right place to put the api key??

class Web3UserHistoryHandler:
    
    def __init__(self):
        self.contract_abi = self.get_contract_abi()
        self.web3_connection = self.get_web3_connection_instance()
        self.contract_instance = self.web3_connection.eth.contract(address=CONTRACT_ADDRESS, abi=self.contract_abi)



    def authenticate_wallet(self, wallet_address: str, wallet_private_key: str) -> bool:
        """
        Authenticates the wallet by signing a message with the private key and verifying the signature.

        Returns:
            bool: True if the private key matches the wallet address, False otherwise.
        """
        message = "Authenticate wallet"
        message_hash = self.web3_connection.keccak(text=message)
        defunct_message = encode_defunct(message_hash)
        
        signed_message = self.web3_connection.eth.account.sign_message(
            defunct_message,
            private_key=wallet_private_key
        )

        recovered_address = self.web3_connection.eth.account.recover_message(
            defunct_message,
            signature=signed_message.signature
        )

        # Check if the recovered address matches the provided wallet address
        return recovered_address.lower() == wallet_address.lower()

    def get_web3_connection_instance(self) -> Web3:
        '''
        Establishes a connection to the Sepolia Testnet.

        Returns:
            Web3: An instance of the Web3 class connected to the Sepolia Testnet.
            None: If the connection fails.
        '''
        sepolia_url = 'https://sepolia.infura.io/v3/' + SEPOLIA_API_KEY
        w3 = Web3(Web3.HTTPProvider(sepolia_url))       
        return w3 if w3.is_connected() else None

    def get_contract_abi(self):

        response = requests.get(f"{SERVER_URL}/get_contract_abi", params={'contract_address': CONTRACT_ADDRESS})
        return response.json() if response.status_code == 200 else ''
        
    def get_user_history(self, account_address: str) -> dict:
        if not self.contract_instance.functions.addressExists(account_address).call():
            return {}
        user_data_bytes = self.contract_instance.functions.retrieveData().call({'from': account_address})
        user_data = json.loads(user_data_bytes.decode('utf-8'))
        return user_data 
    
    def update_user_history(self, user_data: dict, account_address: str, private_key: str) -> str:
        """

        """
        data_bytes = json.dumps(user_data).encode('utf-8')
        tx_function = self.contract_instance.functions.storeData(data_bytes)

        # Prepare the transaction that will store data
        store_txn = tx_function.build_transaction({
            'chainId': self.web3_connection.eth.chain_id,
            'from': account_address,
            'nonce': self.web3_connection.eth.get_transaction_count(account_address),
            'gas': tx_function.estimate_gas({'from': account_address}),
        })

        signed_tx = self.web3_connection.eth.account.sign_transaction(store_txn, private_key)
        tx_hash = self.web3_connection.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt.transactionHash.hex()

    def clear_user_history(self, account_address: str, private_key: str) -> str:

        # Prepare the transaction
        tx_function = self.contract_instance.functions.clearData()

        clear_data_txn = tx_function.build_transaction({
            'chainId': self.web3_connection.eth.chain_id,
            'from': account_address,
            'nonce': self.web3_connection.eth.get_transaction_count(account_address),
            'gas': tx_function.estimate_gas({'from': account_address}),
        })

        
        signed_tx = self.web3_connection.eth.account.sign_transaction(clear_data_txn, private_key)
        tx_hash = self.web3_connection.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3_connection.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.transactionHash.hex()



# w3_client = Web3UserHistoryHandler()
# adress = '0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B'
# private_key = '7adf8381908aee6ee141616efb1f74a5f76278f66a1a83b1178e364db0d3969a'
# print(w3_client.authenticate_wallet(adress, private_key))



# d ={'s':{ 'a': 1, 'b': 2, 'c': 3}, 't':{ 'a': 1, 'b': 2, 'c': 3}}
# d_json = json.dumps(d)
# print(d_json)
# print(type(d_json))
# # turn the json string back to a dictionary
# d_dict = json.loads(d_json)
# print(d_dict)
# print(type(d_dict))





# Connect to Sepolia testnet
# sepolia_url = 'https://sepolia.infura.io/v3/a32106b340fb4f1aa81105e66a70b2ff'
# w3 = Web3(Web3.HTTPProvider(sepolia_url))

# # Ensure connection is successful
# if w3.is_connected():
#     print("Connected to Sepolia Testnet")
# else:
#     print("Failed to connect to Sepolia Testnet\n\n\n")

# # Your contract details
# contract_address = '0x158ca7e48d81031f9fF65425b4B084ECd1853107'

# contract_abi = 


# contract_abi = json.loads(utils.ABI)  # Replace YOUR_CONTRACT_ABI with the actual ABI json string

# # Initialize contract
# contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# #Example of reading from the contract (a public variable or a function that doesn't change state)
# #Replace 'example_read_function' with your actual function name
# read_result = contract.functions.retrive().call()
# print(f"Read Result: {read_result}")
# print("\n\n\n---------------------------------------------------\n\n\n")

# # Example of writing to the contract (requires a transaction)
# # Replace 'example_write_function' and 'FUNCTION_ARGUMENTS' with your actual function and arguments
# tx_function = contract.functions.store (0x6057361d)(121234)
# wallet_address = '0x5441f3581Ba3c9193832Bb5b2c44487E4BB0190B'
# wallet_private_key = '7adf8381908aee6ee141616efb1f74a5f76278f66a1a83b1178e364db0d3969a'

# # Estimate gas for the transaction
# gas_estimate = tx_function.estimate_gas({'from': wallet_address})

# # Get current nonce for the wallet
# nonce = w3.eth.get_transaction_count(wallet_address)# Create transaction dictionary
# tx = tx_function.build_transaction({
#     'chainId': w3.eth.chain_id,
#     'gas': gas_estimate,
#     'nonce': nonce,
# })

# # Sign the transaction
# signed_tx = w3.eth.account.sign_transaction(tx, wallet_private_key)

# # Send the transaction
# tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# # Wait for transaction receipt (optional, for confirmation)
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")


    