
from kraken.auth import build_headers
from kraken.request import urljoin, urlencode


class Kraken:

    api_url = 'api.kraken.com'
    api_version = 0

    def get_server_time(self):
        return self.build_request(method='GET', end_point='public/Time')

    def get_assert_info(self):
        return self.build_request(method='GET', end_point='public/Assets')

    def get_tradable_asset_pairs(self):
        return self.build_request(method='GET', end_point='public/AssetPairs')

    def get_ticker_information(self, pair):
        return self.build_request(method='GET', end_point='public/Ticker')

    def get_ohlc(self):
        return self.build_request(method='GET', end_point='public/OHLC')

    def get_order_book(self, pair):
        return self.build_request(method='GET', end_point='public/Depth')

    def get_recent_trades(self):
        return self.build_request(method='GET', end_point='public/Trades')

    def get_recent_spread(self):
        return self.build_request(method='GET', end_point='public/Spread')

    def build_request(self, method, end_point, data=None):
        #TODO
        url = urljoin(self.api_url, self.api_version, end_point)
        headers = build_headers(end_point, data)
        return dict(method=method, url=url, headers=headers, data=data)
