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
    
    # 2. API configuration with Headers to bypass simple blocks
    API_BASE = "https://toncenter.com/api/v2"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 3. Setup Wallet
    mnemonics_list = mnemonic.split()
    _m, _pub, _priv, wallet = Wallets.from_mnemonics(mnemonics_list, version='v4r2', workchain=0)
    wallet_address = wallet.address.to_string(True, True, False)
    
    print(f"Checking wallet: {wallet_address}")

    # 4. Get Sequence Number (seqno) with error handling
    seqno = 0
    try:
        # Added headers to the request
        response = requests.get(f"{API_BASE}/getAddressInformation?address={wallet_address}", headers=headers)
        
        if response.status_code != 200:
            print(f"API Error: Status {response.status_code}. The API might be blocking the request.")
            return

        data = response.json()
        seqno = data.get('result', {}).get('seqno', 0)
        if seqno is None: seqno = 0
        print(f"Current seqno: {seqno}")
    except Exception as e:
        print(f"Could not parse JSON. The server sent: {response.text[:100]}")
        return

    # 5. Create Transfer
    query = wallet.create_transfer_message(
        to_addr=recipient,
        amount=to_nano(amount, 'ton'),
        seqno=int(seqno),
        payload=memo
    )

    # 6. Broadcast to Network
    boc = base64.b64encode(query['boc'].to_boc(False)).decode()
    payload = {"boc": boc}
    
    # Small delay before sending
    time.sleep(1)
    
    response = requests.post(f"{API_BASE}/sendBoc", json=payload, headers=headers)
    
    if response.status_code == 200:
        print(f"Successfully sent! Response: {response.json()}")
    else:
        print(f"Failed to send. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
