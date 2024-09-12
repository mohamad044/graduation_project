from web3 import Web3
# from web3.middleware import geth_poa_middleware

# Connect to the local Ethereum node (Ganache in this case)
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# Inject Geth's Proof of Authority middleware if using Ganache or a PoA chain
#w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if the connection is successful
if not w3.is_connected():
    raise Exception("Failed to connect to the blockchain.")

# Convert the contract address to a checksum address
contract_address = '0x4900c35add939cebedac00ee3e74360c023a06ef'  # Replace with your contract address
contract_address_checksum = w3.to_checksum_address(contract_address)

# ABI (Application Binary Interface) of the contract
abi = [
    {
        "constant": False,
        "inputs": [{"name": "_hash", "type": "string"}],
        "name": "storeHash",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_hash", "type": "string"}],
        "name": "checkHash",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Load the contract using the checksum address
contract = w3.eth.contract(address=contract_address_checksum, abi=abi)

# Function to store hash in the blockchain
def store_hash_in_blockchain(file_hash):
    # Specify the Ethereum account to send the transaction from
    account = w3.eth.accounts[0]  # Replace with your account if needed

    # Specify the gas limit and gas price (if desired, or let Web3 handle it)
    gas_limit = 2000000  # Set gas limit for the transaction
    gas_price = w3.eth.gas_price  # Retrieve the current gas price

    # Send the transaction to store the file hash in the blockchain
    tx_hash = contract.functions.storeHash(file_hash).transact({
        'from': account,
        'gas': gas_limit,
        'gasPrice': gas_price
    })

    # Wait for the transaction receipt to confirm it was mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    return tx_receipt

def get_hash(file_hash):
       # Specify the Ethereum account to send the transaction from
    account = w3.eth.accounts[0]  # Replace with your account if needed

    # Specify the gas limit and gas price (if desired, or let Web3 handle it)
    gas_limit = 2000000  # Set gas limit for the transaction
    gas_price = w3.eth.gas_price  # Retrieve the current gas price

    # Send the transaction to store the file hash in the blockchain
    tx_hash = contract.functions.checkHash(file_hash).transact({
        'from': account,
        'gas': gas_limit,
        'gasPrice': gas_price
    })

    # Wait for the transaction receipt to confirm it was mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    return tx_receipt


# Example of usage (you can call this in your Django view):
# file_hash = 'your_file_hash_here'
# tx_receipt = store_hash_in_blockchain(file_hash)
# print(f"Stored hash transaction: {tx_receipt}")
