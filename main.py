import os
import asyncio
import requests
from pytoniq import LiteClient, WalletV4R2

# Load secrets from Railway Variables
MNEMONIC = os.getenv("MNEMONIC")
RECIPIENT = "UQB3jmbybhCXQqyKHShHp5R_6Za8Wbdo4MHShl2Ky-xZwRL6" # Change to your target address
AMOUNT = 0.03                # Amount in TON (e.g., 0.5)

async def main():
    if not MNEMONIC:
        print("❌ Error: MNEMONIC variable is empty in Railway!")
        return

    # 1. Get Network Config
    config_url = "https://ton.org"
    config = requests.get(config_url).json()

    # 2. Connect to LiteServer
    client = LiteClient.from_config(config)
    await client.connect()

    try:
        # 3. Initialize Wallet
        # This signs everything locally on Railway
        wallet = await WalletV4R2.from_mnemonic(client, MNEMONIC.split())
        
        print(f"✅ Wallet Address: {wallet.address.to_str()}")
        
        # 4. Send Transfer
        # amount is in NanoTON (1 TON = 1,000,000,000 NanoTON)
        print(f"🚀 Sending {AMOUNT} TON...")
        await wallet.transfer(
            destination=RECIPIENT,
            amount=int(AMOUNT * 1e9), 
            comment="Railway Secure Local Sign"
        )
        
        print("🎉 Transfer sent successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())

