import asyncio
import requests
import base64
import time
from tonsdk.contract.wallet import Wallets
from tonsdk.utils import to_nano

async def main():
    # 1. Your Data
    mnemonic = "funny oblige mushroom bread hollow tape base enemy dinosaur genuine smooth enact before venue border cover trigger pluck antenna holiday crack main dance either"
    recipient = "UQB5hKk2ZjEEjN1d7SQJxMGr-CGcmT0moFlVlr1BDGC7iS8d"
    amount = 0.03
    memo = "115493"
    
    API_BASE = "https://toncenter.com"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 2. Setup Wallet (Using v4r2 to match your UQ... address)
    mnemonics_list = mnemonic.split()
    _m, _pub, _priv, wallet = Wallets.from_mnemonics(mnemonics_list, version='v4r2', workchain=0)
    wallet_address = wallet.address.to_string(True, True, False)
    
    print(f"Checking wallet: {wallet_address}")

    # 3. Get Sequence Number (seqno)
    seqno = 0
    try:
        response = requests.get(f"{API_BASE}/getAddressInformation?address={wallet_address}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            seqno = data.get('result', {}).get('seqno', 0)
            if seqno is None: seqno = 0
        print(f"Current seqno: {seqno}")
    except Exception as e:
        print(f"Seqno fetch failed, trying with 0. Error: {e}")

    # 4. Create Transfer (Fixed the 'boc' access)
    # The library returns an object, so we call .to_boc() on it directly
    query = wallet.create_transfer_message(
        to_addr=recipient,
        amount=to_nano(amount, 'ton'),
        seqno=int(seqno),
        payload=memo
    )

    # 5. Broadcast to Network
    # Accessing 'message' instead of 'boc' and converting to base64
    boc_bytes = query['message'].to_boc(False)
    boc_base64 = base64.b64encode(boc_bytes).decode()
    
    payload = {"boc": boc_base64}
    response = requests.post(f"{API_BASE}/sendBoc", json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"Successfully sent! Response: {response.json()}")
    else:
        print(f"Failed to send. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
