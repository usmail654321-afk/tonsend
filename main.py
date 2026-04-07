import os
import asyncio
import requests

from tonutils.client import TonClient
from tonutils.wallet import WalletV4R2


# 🔐 নিরাপদভাবে Railway Variables থেকে mnemonic নাও
SEED_PHRASE = os.getenv("MNEMONIC")

# 🎯 যেখানে পাঠাবে
RECIPIENT = "UQB3jmbybhCXQqyKHShHp5R_6Za8Wbdo4MHShl2Ky-xZwRL6"  # এখানে নিজের address দাও

# 💰 কত TON পাঠাবে
AMOUNT = 0.02


async def main():
    if not SEED_PHRASE:
        print("❌ Error: MNEMONIC environment variable is not set.")
        return

    # 🌐 TON config load
    config_url = "https://ton.org/global-config.json"
    config = requests.get(config_url).json()

    # 🔌 Client create
    client = TonClient(config=config)

    try:
        # 🔗 Connect to network
        await client.connect()

        # 🔑 mnemonic split
        mnemonic_list = SEED_PHRASE.split()

        # 💼 Wallet তৈরি
        wallet = WalletV4R2.from_mnemonic(
            client=client,
            mnemonics=mnemonic_list
        )

        print(f"✅ Connected Wallet: {wallet.address}")

        # 🚀 Transfer start
        print(f"🚀 Sending {AMOUNT} TON to {RECIPIENT}...")

        tx_hash = await wallet.transfer(
            destination=RECIPIENT,
            amount=AMOUNT,
            comment="Railway Auto Transfer"
        )

        print(f"🎉 Success! TX Hash: {tx_hash}")

    except Exception as e:
        print(f"❌ Error during transfer: {e}")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())

