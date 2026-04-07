import os
import asyncio

from pytoniq import LiteClient
from pytoniq.contract.wallets import WalletV4R2

# 💰 Settings
RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
AMOUNT = 0.02  # TON
SEED_PHRASE = os.getenv("MNEMONIC")


async def main():
    print("🚀 Starting TON bot...")

    if not SEED_PHRASE:
        print("❌ MNEMONIC not set in Railway variables")
        return

    try:
        # ✅ Connect to Mainnet LiteClient
        client = LiteClient.from_mainnet()
        await client.connect()
        print("✅ Connected to TON Mainnet")

        # Load Wallet
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(client=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # Convert TON -> nanoTON
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
