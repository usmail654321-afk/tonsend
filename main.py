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
    
    # Using Tonapi.io (More reliable for cloud services)
    API_BASE = "https://tonapi.io"
    
    # 2. Setup Wallet
    mnemonics_list = mnemonic.split()
    _m, _pub, _priv, wallet = Wallets.from_mnemonics(mnemonics_list, version='v4r2', workchain=0)
    wallet_address = wallet.address.to_string(True, True, False)
    print(f"Checking wallet: {wallet_address}")

    # 3. Get Sequence Number (seqno) from Tonapi
    seqno = 0
    try:
        response = requests.get(f"{API_BASE}/blockchain/accounts/{wallet_address}/methods/seqno")
        if response.status_code == 200:
            data = response.json()
            # Tonapi returns { "success": true, "decoded": { "stack": [...] } }
            stack = data.get('decoded', {}).get('stack', [])
            if stack:
                seqno = int(stack[0].get('num', 0), 16) if '0x' in str(stack[0].get('num')) else int(stack[0].get('num', 0))
        print(f"Current seqno: {seqno}")
    except Exception as e:
        print(f"Seqno fetch failed, using 0. Error: {e}")

    # 4. Create Transfer
    query = wallet.create_transfer_message(
        to_addr=recipient,
        amount=to_nano(amount, 'ton'),
        seqno=int(seqno),
        payload=memo
    )

    # 5. Broadcast to Network via Tonapi
    boc_bytes = query['message'].to_boc(False)
    boc_base64 = base64.b64encode(boc_bytes).decode()
    
    payload = {"boc": boc_base64}
    # Tonapi uses /v2/blockchain/message
    response = requests.post(f"{API_BASE}/blockchain/message", json=payload)
    
    if response.status_code == 200:
        print(f"Successfully sent! Transaction accepted by Tonapi.")
    else:
        print(f"Failed to send. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(main())
