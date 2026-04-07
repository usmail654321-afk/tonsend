import os
import asyncio
from pytoniq import LiteClient
from pytoniq.contract.wallets import WalletV4R2

# Settings
RECIPIENT = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
AMOUNT = 0.02  # TON
SEED_PHRASE = os.getenv("MNEMONIC")

# Public Mainnet LiteServer
LITE_SERVER = {
    "host": "main.ton.dev",
    "port": 443,
    "server_pub_key": bytes.fromhex(
        "a5c2c34b5b8b2f7c5e53d6d3b18fae6827b4313d38a0bb1f2f1f3e0b6d2c4a8f"
    ),
}

async def main():
    print("🚀 Starting TON bot...")

    if not SEED_PHRASE:
        print("❌ MNEMONIC not set in Railway variables")
        return

    client = None
    try:
        # Connect LiteClient
        print(f"🔗 Connecting to TON server {LITE_SERVER['host']}:{LITE_SERVER['port']}...")
        client = LiteClient(
            host=LITE_SERVER["host"],
            port=LITE_SERVER["port"],
            server_pub_key=LITE_SERVER["server_pub_key"]
        )
        await client.connect()
        print("✅ Connected to TON network")

        # Load Wallet
        mnemonics = SEED_PHRASE.split()
        wallet = await WalletV4R2.from_mnemonic(provider=client, mnemonics=mnemonics)
        print(f"✅ Wallet loaded: {wallet.address}")

        # Balance check
        balance = await client.get_address_balance(wallet.address)
        print(f"💎 Current Balance: {balance / 1e9} TON")

        # Transfer
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
