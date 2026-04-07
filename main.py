import os
import asyncio
import requests
from tonutils.client import LiteserverClient
from tonutils.wallet import WalletV4R2

# Safely load your seed phrase from Railway's "Variables" tab
# Never write the actual words in this file!
SEED_PHRASE = os.getenv("MNEMONIC")
RECIPIENT = "UQB3jmbybhCXQqyKHShHp5R_6Za8Wbdo4MHShl2Ky-xZwRL6" # Put the address you want to send to
AMOUNT = 0.02                # Amount in TON

async def main():
    if not SEED_PHRASE:
        print("❌ Error: MNEMONIC environment variable is not set.")
        return

    # 1. Connect directly to TON network without an API key
    config_url = "https://ton.org"
    config = requests.get(config_url).json()
    client = LiteserverClient(config=config)
    await client.connect()

    try:
        # 2. Setup your wallet locally
        mnemonic_list = SEED_PHRASE.split()
        wallet = WalletV4R2.from_mnemonic(client, mnemonics=mnemonic_list)
        print(f"✅ Connected to Wallet: {wallet.address}")

        # 3. Send the transfer
        print(f"🚀 Sending {AMOUNT} TON to {RECIPIENT}...")
        tx_hash = await wallet.transfer(
            destination=RECIPIENT,
            amount=AMOUNT,
            comment="Railway Secure Transfer"
        )
        print(f"🎉 Success! Transaction Hash: {tx_hash}")

    except Exception as e:
        print(f"❌ Error during transfer: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())

