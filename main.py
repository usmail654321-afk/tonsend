import os
import asyncio
import requests

from pytoniq import LiteClient
from pytoniq.contract.wallets import WalletV4R2


# 🔐 Railway Variables থেকে mnemonic নাও
SEED_PHRASE = os.getenv("MNEMONIC")

# 🎯 Receiver Address
RECIPIENT = "UQB3jmbybhCXQqyKHShHp5R_6Za8Wbdo4MHShl2Ky-xZwRL6"   # নিজের address বসাও

# 💰 Amount in TON
AMOUNT = 0.02


async def main():
    if not SEED_PHRASE:
        print("❌ Error: MNEMONIC not set in Railway Variables")
        return

    try:
        # 🌐 TON config load
        config_url = "https://ton.org/global-config.json"
        config = requests.get(config_url).json()

        # 🔌 Connect LiteClient
        client = LiteClient.from_mainnet_config(config)
        await client.connect()

        # 🔑 mnemonic list
        mnemonics = SEED_PHRASE.split()

        # 💼 Wallet load
        wallet = await WalletV4R2.from_mnemonic(
            client=client,
            mnemonics=mnemonics
        )

        print(f"✅ Wallet Connected: {wallet.address}")

        # 💸 TON → nanoTON convert (VERY IMPORTANT)
        amount_nano = int(AMOUNT * 1_000_000_000)

        print(f"🚀 Sending {AMOUNT} TON to {RECIPIENT}...")

        # 📤 Send transaction
        tx_hash = await wallet.transfer(
            destination=RECIPIENT,
            amount=amount_nano,
            comment="Railway Auto Transfer"
        )

        print(f"🎉 SUCCESS! TX HASH: {tx_hash}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    finally:
        try:
            await client.close()
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())

