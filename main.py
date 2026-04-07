import os
import asyncio
from pytoniq import LiteClient, WalletV4R2

# 💰 Settings
RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
AMOUNT = 0.02  # TON
SEED_PHRASE = os.getenv("MNEMONIC")

async def main():
    print("🚀 Starting TON bot...")

    if not SEED_PHRASE:
        print("❌ MNEMONIC not set in Railway variables")
        return

    client = None
    try:
        # 1. Initialize and connect the LiteClient
        client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2)
        await client.connect()
        print("✅ Connected to TON network")

        # 2. Load Wallet (Use 'provider' instead of 'client')
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(provider=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # 3. Convert TON to nanoTON
        amount_nano = int(AMOUNT * 1_000_000_000)

        # 4. Transfer
        print(f"💸 Sending {AMOUNT} TON to {RECIPIENT}...")
        # Since 'provider' was passed above, we don't need 'client' here
        tx_hash = await wallet.transfer(
            destination=RECIPIENT, 
            amount=amount_nano, 
            comment="Railway Auto Transfer"
        )
        print(f"🎉 Transfer SUCCESS! TX HASH: {tx_hash}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    finally:
        if client:
            await client.close()
            print("✅ Client closed")

if __name__ == "__main__":
    asyncio.run(main())

