import os
import asyncio
import requests

from pytoniq import LiteClient
from pytoniq.contract.wallets import WalletV4R2

RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
AMOUNT = 0.02  # TON
SEED_PHRASE = os.getenv("MNEMONIC")


async def main():
    print("🚀 Starting TON bot...")

    if not SEED_PHRASE:
        print("❌ MNEMONIC not set in Railway variables")
        return

    try:
        # ⚡ Load LiteServer config from mainnet
        config_url = "https://ton.org/global-config.json"
        global_config = requests.get(config_url).json()
        lite_servers = global_config.get("lite_servers", [])
        if not lite_servers:
            raise ValueError("Lite servers not found in global config")
        print(f"✅ Loaded {len(lite_servers)} lite servers")

        # Connect LiteClient
        client = LiteClient(servers=lite_servers)
        await client.connect()
        print("✅ Connected to TON network")

        # Load Wallet
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(client=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # Convert to nanoTON
        amount_nano = int(AMOUNT * 1_000_000_000)

        print(f"💸 Sending {AMOUNT} TON to {RECIPIENT}...")
        tx_hash = await wallet.transfer(destination=RECIPIENT, amount=amount_nano, comment="Railway Auto Transfer")
        print(f"🎉 Transfer SUCCESS! TX HASH: {tx_hash}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    finally:
        try:
            await client.close()
            print("✅ Client closed")
        except:
            pass


if __name__ == "__main__":
    asyncio.run(main())
