
from kraken.api import Kraken
from ratelimit import rate_limited


kraken = Kraken()
kraken.process = rate_limited(1, 3)(kraken.process)


def test_get_trade_balance():
    result = kraken.get_trade_balance()
    print(result)


def test_get_trades_history():
    result = kraken.get_trades_history()
    print(result)
