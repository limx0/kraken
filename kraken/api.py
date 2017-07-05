
from kraken.auth import build_headers


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

    def get_trade_balance(self, asset_class, asset):
        data = {'aclass': asset_class, 'asset': asset}
        return self.build_request(method='POST', end_point='private/TradeBalance', data=data)

    def get_open_orders(self, trades=True, user_ref=None):
        data = {'trades': str(trades).lower(), 'userref': user_ref}
        return self.build_request(method='POST', end_point='private/OpenOrders', data=data)

    def build_request(self, method, end_point, data=None):
        headers = None
        end_point = '/%s/%s' % (self.api_version, end_point)
        if method == 'POST':
            headers = build_headers(end_point, data)
            data = data or {}
            data.update({'nonce': headers.pop('nonce')})
        return dict(method=method, url=self.base_url + end_point, headers=headers, data=data)
