
import os
import time
import hmac
import base64
import hashlib
from kraken.request import urlencode


def build_headers(url, data):

    api_key = os.environ['KRAKEN_API_KEY']
    secret = os.environ['KRAKEN_SECRET']

    data = data
    nonce = int(1000 * time.time())
    data.update({'nonce': nonce})

    # Unicode-objects must be encoded before hashing
    encoded = (str(nonce) + urlencode(data)).encode()
    message = url.encode() + hashlib.sha256(encoded).digest()
    rsig = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    bsig = base64.b64encode(rsig.digest())

    return {
        'API-Key': api_key,
        'API-Sign': bsig.decode(),
    }
