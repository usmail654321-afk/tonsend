import asyncio
import requests
import base64
from tonsdk.contract.wallet import Wallets
from tonsdk.utils import to_nano

async def main():
    # 1. Your Data
    mnemonic = "funny oblige mushroom bread hollow tape base enemy dinosaur genuine smooth enact before venue border cover trigger pluck antenna holiday crack main dance either"
    recipient = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
    amount = 0.03
    memo = "115493"
    
    # API configuration
    API_BASE = "https://toncenter.com"
    
    # 2. Setup Wallet (Fixed function name: from_mnemonics)
    mnemonics_list = mnemonic.split()
    # Changed from_mnemonic to from_mnemonics
    _m, _pub, _priv, wallet = Wallets.from_mnemonics(mnemonics_list, version='v4r2', workchain=0)
    wallet_address = wallet.address.to_string(True, True, False)
    
    print(f"Checking wallet: {wallet_address}")

    # 3. Get Sequence Number (seqno) from API
    try:
        res = requests.get(f"{API_BASE}/getAddressInformation?address={wallet_address}").json()
        # If wallet is not initialized, seqno won't be in the response
        seqno = res.get('result', {}).get('seqno', 0)
        if seqno is None: seqno = 0
    except Exception as e:
        print(f"Error fetching seqno: {e}")
        return

    # 4. Create Transfer
    query = wallet.create_transfer_message(
        to_addr=recipient,
        amount=to_nano(amount, 'ton'),
        seqno=int(seqno),
        payload=memo
    )

    # 5. Broadcast to Network
    boc = base64.b64encode(query['boc'].to_boc(False)).decode()
    
    payload = {"boc": boc}
    response = requests.post(f"{API_BASE}/sendBoc", json=payload)
    
    if response.status_code == 200:
        print(f"Successfully sent! Response: {response.json()}")
    else:
        print(f"Failed to send. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
