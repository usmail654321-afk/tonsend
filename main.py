import os
import asyncio
import requests

from pytoniq import LiteClient
from pytoniq.contract.wallets import WalletV4R2

# Railway Variables থেকে mnemonic নাও
SEED_PHRASE = os.getenv("MNEMONIC")

# পাঠানোর address
RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"  # নিজের address বসাও

# Amount in TON
AMOUNT = 0.03


async def main():
    if not SEED_PHRASE:
        print("❌ Error: MNEMONIC not set")
        return

    try:
        # TON config load
        config_url = "https://ton.org/global-config.json"
        config = requests.get(config_url).json()

        # Connect LiteClient
        client = LiteClient.from_mainnet_config(config)
        await client.connect()

        # Load wallet from mnemonic
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(
            client=client,
            mnemonics=mnemonics
        )

        print(f"✅ Wallet: {wallet.address}")

        # TON -> nanoTON
        amount_nano = int(AMOUNT * 1_000_000_000)

        print(f"🚀 Sending {AMOUNT} TON to {RECIPIENT}...")

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
