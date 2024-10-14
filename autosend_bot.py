import os
import time
import logging
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Connect to Ethereum network using Infura or Alchemy
INFURA_URL = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Wallet credentials (load from environment variables)
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
RECIPIENT_ADDRESS = os.getenv('RECIPIENT_ADDRESS')
AMOUNT_TO_SEND = web3.to_wei(0.01, 'ether')  # Set default amount

# Check connection to the network
if web3.is_connected():
    logging.info(f"Connected to Ethereum network at {INFURA_URL}")
else:
    logging.error("Failed to connect to the Ethereum network.")
    exit()

def send_ether():
    try:
        # Get the current nonce for the sender's wallet
        nonce = web3.eth.getTransactionCount(SENDER_ADDRESS)

        # Estimate gas and gas price dynamically
        gas_price = web3.eth.gas_price
        logging.info(f"Current gas price: {web3.fromWei(gas_price, 'gwei')} gwei")

        # Create the transaction object
        tx = {
            'nonce': nonce,
            'to': RECIPIENT_ADDRESS,
            'value': AMOUNT_TO_SEND,
            'gas': 21000,  # Default for sending Ether
            'gasPrice': gas_price,
            'chainId': 1  # Mainnet; adjust for other networks
        }

        # Sign the transaction
        signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info(f'Transaction sent: {web3.toHex(tx_hash)}')

        # Wait for confirmation
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logging.info(f"Transaction confirmed in block {tx_receipt.blockNumber}")

    except Exception as e:
        logging.error(f"Error during transaction: {e}")
        # Retry mechanism could go here or alerting the user via messaging services (e.g., Telegram)
        return False

    return True

# Main loop to send Ether at regular intervals
def main():
    while True:
        success = send_ether()
        if success:
            logging.info(f"Successfully sent {web3.fromWei(AMOUNT_TO_SEND, 'ether')} ETH to {RECIPIENT_ADDRESS}")
        else:
            logging.error("Failed to send Ether.")

        # Sleep for 1 hour (3600 seconds) before sending again
        time.sleep(3600)

if __name__ == '__main__':
    main()
