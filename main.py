import os
import asyncio
import httpx  # Using httpx for reliable async fetching
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

    # 1. Fetch fresh config manually via httpx
    # This avoids the "list index out of range" error from the SDK's internal fetcher
    try:
        async with httpx.AsyncClient() as http:
            resp = await http.get('https://ton.org')
            config = resp.json()
    except Exception as e:
        print(f"❌ Failed to fetch TON config: {e}")
        return

    client = None
    # 2. Try each server in the config until one works
    for i in range(len(config['liteservers'])):
        try:
            print(f"🔗 Trying LiteServer #{i}...")
            client = LiteClient.from_config(config, ls_i=i, trust_level=1)
            await client.connect()
            print(f"✅ Connected to server #{i}")
            break 
        except Exception as e:
            print(f"⚠️ Server #{i} failed: {e}")
            if client: await client.close()
            client = None

    if not client:
        print("❌ Could not connect to any TON LiteServers.")
        return

    try:
        # 3. Load Wallet
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(provider=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # 4. Transfer
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
        if client:
            await client.close()
            print("✅ Client closed")

if __name__ == "__main__":
    asyncio.run(main())
