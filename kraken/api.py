
from urllib.parse import urlencode
from kraken.auth import build_headers

from kraken.util import clean_locals


class Kraken:

    base_url = 'https://api.kraken.com'
    api_version = '0'

    def get_server_time(self):
        return self.build_request(method='GET', end_point='public/Time')

    def get_assert_info(self):
        return self.build_request(method='GET', end_point='public/Assets')

    def get_tradable_asset_pairs(self):
        return self.build_request(method='GET', end_point='public/AssetPairs')

    def get_ticker_information(self, pair):
        data = {'pair': pair}
        return self.build_request(method='POST', end_point='public/Ticker', data=data)

    def get_ohlc(self):
        return self.build_request(method='GET', end_point='public/OHLC')

    def get_order_book(self, pair):
        data = {'pair': pair}
        return self.build_request(method='POST', end_point='public/Depth', data=data)

    def get_recent_trades(self):
        return self.build_request(method='GET', end_point='public/Trades')

    def get_recent_spread(self):
        return self.build_request(method='GET', end_point='public/Spread')

    def get_account_balance(self):
        return self.build_request(method='POST', end_point='private/Balance')

    def get_trade_balance(self, asset_class='currency', asset='ZUSD'):
        data = {'aclass': asset_class, 'asset': asset}
        return self.build_request(method='POST', end_point='private/TradeBalance', data=data)

    def get_open_orders(self, trades=True, user_ref=None):
        data = {'trades': str(trades).lower(), 'userref': user_ref}
        return self.build_request(method='POST', end_point='private/OpenOrders', data=data)

    def get_closed_orders(self, trades, user_ref, start, end, offset, close_time):
        """
        trades = whether or not to include trades in output (optional.  default = false)
        userref = restrict results to given user reference id (optional)
        start = starting unix timestamp or order tx id of results (optional.  exclusive)
        end = ending unix timestamp or order tx id of results (optional.  inclusive)
        ofs = result offset
        closetime = which time to use (optional)
            open
            close
            both (default)
        """
        data = {
            'trades': trades, 'userref': user_ref, 'start': start, 'end': end, 'ofs': offset, 'closetime': close_time
        }
        return self.build_request(method='POST', end_point='private/ClosedOrders', data=data)

    def query_order_info(self):
        pass

    def get_trades_history(self):
        pass

    def get_open_positions(self, txid=None, docalcs=None):
        data = {'txid': txid, 'docalcs': str(docalcs).lower()}
        return self.build_request(method='POST', end_point='private/OpenPositions', data=data)

    def build_request(self, method, end_point, data=None):
        headers = None
        end_point = '/%s/%s' % (self.api_version, end_point)
        if method == 'POST':
            headers = build_headers(end_point, data)
            data = data or {}
            data.update({'nonce': headers.pop('nonce')})
            data = {k: v for k, v in data.items() if v is not None}
            data = urlencode(data)
        return dict(method=method, url=self.base_url + end_point, headers=headers, data=data)
