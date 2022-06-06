from binascii import unhexlify
import datetime
import os
import requests
from symbolchain.CryptoTypes import PrivateKey
from symbolchain.symbol.KeyPair import KeyPair
from symbolchain.facade.SymbolFacade import SymbolFacade

priv_key_hex = os.getenv("PRIVATE_KEY")
address = os.getenv("ADDRESS")
node = "http://01.symbol-blockchain.com:3000"
birthtime = 1615853185
mosaic_id = 0x606F8854012B0C0F

facade = SymbolFacade("mainnet")

priv_key = PrivateKey(unhexlify(priv_key_hex))
key_pair = KeyPair(priv_key)
pub_key = key_pair.public_key

deadline = (
    int((datetime.datetime.today() + datetime.timedelta(hours=2)).timestamp()) - birthtime
) * 1000
amount = 1 * 100000
fee = 1 * 100000
message = "cigarette:smoked"

tx = facade.transaction_factory.create(
    {
        "type": "transfer_transaction",
        "signer_public_key": pub_key,
        "fee": fee,
        "deadline": deadline,
        "recipient_address": address,
        "mosaics": [
            {
                "mosaic_id": mosaic_id,
                "amount": amount,
            },
        ],
        "message": bytes(1) + message.encode("utf-8"),
    }
)

signature = facade.sign_transaction(key_pair, tx)
payload = facade.transaction_factory.attach_signature(tx, signature)

headers = {
    "Content-Type": "application/json"
}

resp = requests.put(node + "/transactions", data=payload, headers=headers)
print(resp.status_code)
