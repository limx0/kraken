
import sys
if sys.version_info > (3, 0):
    from urllib.request import urljoin
    from urllib.parse import urlencode
else:
    from urlparse import urljoin
    from urllib2 import urlencode

session = None


def urllib_request(method, url, headers, data):
    import json
    from urllib.request import urlopen, Request
    if isinstance(data, str):
        data = data.encode("utf-8")
    resp = urlopen(Request(method=method, url=url, headers=headers or {}, data=data))
    return json.loads(resp.read().decode())

