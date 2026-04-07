import os
import asyncio
import httpx
from pytoniq import ToncenterClient, WalletV4R2

# 💰 Settings
RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
AMOUNT = 0.02  # TON
SEED_PHRASE = os.getenv("MNEMONIC")

# TONCenter Public API (No API key needed for low frequency, but good to have)
API_URL = "https://toncenter.com/api/v2/jsonRPC"

async def main():
    print("🚀 Starting TON bot...")

    if not SEED_PHRASE:
        print("❌ MNEMONIC not set in Railway variables")
        return

    # 1. Initialize Client using Toncenter (HTTP-based)
    # This replaces LiteClient and avoids the config download error
    client = ToncenterClient(base_url=API_URL)

    try:
        # 2. Load Wallet
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(provider=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # 3. Check Balance (Safety check)
        balance_nano = await client.get_address_balance(wallet.address)
        print(f"💎 Current Balance: {balance_nano / 1e9} TON")

        if balance_nano < (AMOUNT * 1e9 + 50_000_000): # Amount + ~0.05 for gas
            print("❌ Insufficient funds for transfer + gas fees")
            return

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

if __name__ == "__main__":
    asyncio.run(main())
