
from urllib.parse import urlencode
from kraken.auth import build_headers
from kraken.request import urllib_request
from kraken.enums import Assets, Pairs

class Kraken:

    base_url = 'https://api.kraken.com'
    api_version = '0'

    def __init__(self, request_function=urllib_request, return_kwargs=False):
        self.request = request_function
        self.return_kwargs = return_kwargs

    # Public methods
    def get_server_time(self):
        return self.process(method='GET', end_point='public/Time')

    def get_asset_info(self):
        return self.process(method='GET', end_point='public/Assets')

    def get_tradable_asset_pairs(self):
        return self.process(method='GET', end_point='public/AssetPairs')

    def get_ticker_information(self, pair=Pairs.ETH_XBT):
        data = {'pair': pair}
        return self.process(method='POST', end_point='public/Ticker', data=data)

    def get_ohlc(self):
        return self.process(method='GET', end_point='public/OHLC')

    def get_order_book(self, pair):
        data = {'pair': pair}
        return self.process(method='POST', end_point='public/Depth', data=data)

    def get_recent_trades(self):
        return self.process(method='GET', end_point='public/Trades')

    def get_recent_spread(self):
        return self.process(method='GET', end_point='public/Spread')

    # Private methods
    def get_account_balance(self):
        return self.process(method='POST', end_point='private/Balance')

    def get_trade_balance(self, asset=Assets.USD, asset_class='currency'):
        data = {'aclass': asset_class, 'asset': asset}
        return self.process(method='POST', end_point='private/TradeBalance', data=data)

    def get_open_orders(self, include_trades=True, user_ref=None):
        data = {'trades': include_trades, 'userref': user_ref}
        return self.process(method='POST', end_point='private/OpenOrders', data=data)

    def get_closed_orders(self, trades, user_ref, start, end, offset, close_time):
        """
        trades = whether or not to include trades in output (optional.  default = false)
        user_ref = restrict results to given user reference id (optional)
        start = starting unix timestamp or order tx id of results (optional.  exclusive)
        end = ending unix timestamp or order tx id of results (optional.  inclusive)
        offset = result offset
        close_time = which time to use (optional)
            open
            close
            both (default)
        """
        data = {
            'trades': trades, 'userref': user_ref, 'start': start, 'end': end, 'ofs': offset, 'closetime': close_time
        }
        return self.process(method='POST', end_point='private/ClosedOrders', data=data)

    def query_order_info(self):
        pass

    def get_trades_history(self, trade_type='all', include_trades=False, start=None, end=None, offset=None):
        """
        :param trade_type: type of trade (optional) {'all', 'any position', 'closed position', 'closing position', 'no position'}
        :param include_trades: whether or not to include trades related to position in output (optional.  default = false)
        :param start: starting unix timestamp or trade tx id of results (exclusive)
        :param end: ending unix timestamp or trade tx id of results (inclusive)
        :param offset: result offset
        :return:
        """
        data = {
            'type': trade_type, 'trades': include_trades, 'start': start, 'end': end, 'ofs': offset,
        }
        return self.process(method='POST', end_point='private/TradesHistory', data=data)

    def query_trades_info(self, txid, trades):
        pass

    def get_open_positions(self, txid=None, docalcs=None):
        data = {'txid': txid, 'docalcs': docalcs}
        return self.process(method='POST', end_point='private/OpenPositions', data=data)

    def get_ledgers_info(self):
        pass

    def query_ledgers(self):
        pass
    def get_trade_volume(self):
        pass

    def add_order(self):
        pass

    def cancel_order(self):
        pass

    @staticmethod
    def parse_post_data(data):
        """
        Prepare post data for request
        - Remove None values
        - Convert bool values to lower case strings
        """
        data = data or {}
        keys = list(data.keys())
        for k in keys:
            if data[k] is None:
                data.pop(k)
            elif data[k] in (True, False):
                data[k] = str(data[k]).lower()
        return data

    def build_request(self, method, end_point, data):
        headers = None
        end_point = '/%s/%s' % (self.api_version, end_point)
        if method == 'POST':
            data = self.parse_post_data(data)
            headers = build_headers(end_point, data)
            data = urlencode(data)
        return dict(method=method, url=self.base_url + end_point, headers=headers, data=data)

    def process(self, method, end_point, data=None):
        kwargs = self.build_request(method, end_point, data)
        if self.return_kwargs:
            return kwargs
        response = self.request(**kwargs)
        if response['error']:
            print(kwargs)
            raise Exception(response['error'][0])
        return response['result']
