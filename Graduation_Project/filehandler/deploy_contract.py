from web3 import Web3
from solcx import compile_standard, install_solc,get_installable_solc_versions,set_solc_version

def deploy_contract():
    available_versions = get_installable_solc_versions()
    print(f"Available Solidity versions: {available_versions}")
    
    
    # Install Solidity compiler version
    install_solc('0.6.12')
    set_solc_version('0.6.12')

    # Connect to Ganache
    ganache_url = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url))

    if not w3.is_connected():
        raise Exception("Failed to connect to Ganache")

    # Load the contract source code
    with open('contracts/FileHashStorage.sol', 'r') as file:
        contract_source_code = file.read()

    # Compile the contract
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "FileHashStorage.sol": {"content": contract_source_code}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        }
    })

    # Get ABI and bytecode
    abi = compiled_sol['contracts']['FileHashStorage.sol']['FileHashStorage']['abi']
    bytecode = compiled_sol['contracts']['FileHashStorage.sol']['FileHashStorage']['evm']['bytecode']['object']

    # Set up the account from which to deploy
    account = w3.eth.accounts[0]  # Get the first account from Ganache
    private_key = '0xe02b6fd9ef155048241efe96d521df67b222265e8263c730dbf0a30d1b1b9ac6'

    # Create contract instance in Python
    FileHashStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Build the transaction to deploy the contract
    nonce = w3.eth.get_transaction_count(account)
    transaction = FileHashStorage.constructor().build_transaction({
        'from': account,
        'nonce': nonce,
        'gas': 2000000,  # Set the gas limit
        'gasPrice': w3.eth.gas_price
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction to the blockchain
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress
