import os
import asyncio
from pytoniq import LiteBalancer, WalletV4R2

# 💰 Settings
RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
AMOUNT = 0.02  # TON
SEED_PHRASE = os.getenv("MNEMONIC")

async def main():
    print("🚀 Starting TON bot...")

    if not SEED_PHRASE:
        print("❌ MNEMONIC not set in Railway variables")
        return

    # 1. Use LiteBalancer instead of LiteClient
    # It automatically manages servers and retries for you
    client = LiteBalancer.from_mainnet_config(trust_level=1)
    
    try:
        print("🔗 Connecting and syncing via Balancer...")
        await client.start_up()
        print("✅ Connected to TON network")

        # 2. Load Wallet
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(provider=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # 3. Convert and Transfer
        amount_nano = int(AMOUNT * 1_000_000_000)
        print(f"💸 Sending {AMOUNT} TON to {RECIPIENT}...")
        
        tx_hash = await wallet.transfer(
            destination=RECIPIENT, 
            amount=amount_nano, 
            comment="Railway Auto Transfer"
        )
        print(f"🎉 Transfer SUCCESS! TX HASH: {tx_hash}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    finally:
        # 4. LiteBalancer also uses close()
        await client.close()
        print("✅ Client closed")

if __name__ == "__main__":
    asyncio.run(main())

