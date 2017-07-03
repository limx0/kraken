
import os
import time
import hmac
import base64
import hashlib


def build_headers(end_point, post_data=None):

    api_key = os.environ['KRAKEN_API_KEY'].encode("utf-8")
    secret = os.environ['KRAKEN_SECRET'].encode("utf-8")

    nonce = str(int(time.time() * 1000))
    string_body = end_point + nonce + (post_data or '')
    rsig = hmac.new(base64.standard_b64decode(secret), string_body.encode("utf-8"), hashlib.sha512)
    bsig = base64.standard_b64encode(rsig.digest()).decode("utf-8")

    return {
        ("Accept", "application/json"),
        ("Accept-Charset", "UTF-8"),
        ("Content-Type", "application/json"),
        ("API-Key", api_key.decode("utf-8")),
        ("nonce", nonce),
        ("API-Sign", bsig),
    }
