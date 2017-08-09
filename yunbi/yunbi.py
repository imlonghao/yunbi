#!/usr/bin/env python3

import hmac
import requests
import time
from hashlib import sha256

BASE_URL = 'https://yunbi.com/api/v2/'


class Yunbi():
    def __init__(self, access_key=None, secret_key=None):
        if access_key == None and secret_key == None:
            self.__auth = False
        else:
            self.__auth = True
            self.__access_key = access_key
            self.__secret_key = secret_key

    def __hmac_sha256(self, key, msg):
        hash_obj = hmac.new(key=key, msg=msg, digestmod=sha256)
        return hash_obj.hexdigest()

    def __sign(self, method, url, params):
        message = '%s|/api/v2/%s.json|' % (method, url)
        for i in sorted(params.items()):
            message += '%s=%s&' % (i[0], i[1])
        return self.__hmac_sha256(self.__secret_key.encode(), message[:-1].encode())

    def __public_request(self, method, url, data=None):
        assert method in ['GET', 'POST'], 'Unknow method %s' % method
        data = {} if data is None else data
        if method == 'GET':
            return requests.get(BASE_URL + url + '.json', data=data).json()
        else:
            return requests.post(BASE_URL + url + '.json', data=data).json()

    def __private_request(self, method, url, data=None):
        assert method in ['GET', 'POST'], 'Unknow method %s' % method
        assert self.__auth == True, 'Private API, access_key and secret_key required'
        data = {} if data is None else data
        data['access_key'] = self.__access_key
        tonce = int(time.time() * 1000)
        data['tonce'] = tonce
        signature = self.__sign(method, url, data)
        data['signature'] = signature
        if method == 'GET':
            return requests.get(BASE_URL + url + '.json', data=data).json()
        else:
            return requests.post(BASE_URL + url + '.json', data=data).json()

    def get_markets(self):
        '''Get all available markets.

        :return: :class:`dict`
        '''
        return self.__public_request('GET', 'markets')

    def get_tickers(self):
        '''Get ticker of all markets.

        :return: :class:`dict`
        '''
        return self.__public_request('GET', 'tickers')

    def get_tickers_market(self, market):
        '''Get ticker of specific market.

        :param market: Unique market id
        :return: :class:`dict`
        '''
        return self.__public_request('GET', 'tickers/' + market)

    def get_members_me(self):
        '''Get your profile and accounts info.

        :return: :class:`dict`
        '''
        return self.__private_request('GET', 'members/me')

    def get_deposits(self, **kwargs):
        '''Get your deposits history.

        :param currency: (optional)
        :param limit: (optional) Set result limit
        :param state: (optional)
        :return: :class:`dict`
        '''
        return self.__private_request('GET', 'deposits', kwargs)

    def get_deposit(self, txid):
        '''Get details of specific deposit.

        :param txid:
        :return: :class:`dict`
        '''
        return self.__private_request('GET', 'deposit', {
            'txid': txid
        })

    def get_orders(self, market, **kwargs):
        '''Get your orders, results is paginated.

        :param market: Unique market id
        :param state: (optional) Filter order by state
        :param limit: (optional) Limit the number of returned orders
        :param page: (optional) Specify the page of paginated results
        :param order_by: (optional) If set, returned orders will be sorted in specific order
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        return self.__private_request('GET', 'orders', kwargs)

    def post_orders(self, market, side, volume, **kwargs):
        '''Create a Sell/Buy order.

        :param market: Unique market id
        :param side: Either 'sell' or 'buy'
        :param volume: The amount user want to sell/buy
        :param price: (optional) Price for each unit
        :param ord_type: (optional) Type of order, either 'limit' or 'market'
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        kwargs['side'] = side
        kwargs['volume'] = volume
        return self.__private_request('POST', 'orders', kwargs)

    def post_orders_multi(self, market, orders):
        '''Create multiple sell/buy orders.

        :param market: Unique market id
        :param orders: See the official document
        :return: :class:`dict`
        '''
        return self.__private_request('POST', 'orders/multi', {
            'market': market,
            'orders': orders
        })

    def post_orders_clear(self, **kwargs):
        '''Cancel all my orders.

        :param side: (optional) If present, only sell orders (asks) or buy orders (bids) will be canncelled
        :return: :class:`dict`
        '''
        return self.__private_request('POST', 'orders/clear', kwargs)

    def get_deposit_address(self, currency):
        '''Where to deposit.

        :param currency: The account to which you want to deposit
        :return: :class:`dict`
        '''
        return self.__private_request('GET', 'deposit_address', {
            'currency': currency
        })

    def get_order_book(self, market, **kwargs):
        '''Get the order book of specified market.

        :param market: Unique market id
        :param asks_limit: (optional) Limit the number of returned sell orders
        :param bids_limit: (optional) Limit the number of returned buy orders
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        return self.__public_request('GET', 'order_book', kwargs)

    def get_depth(self, market, **kwargs):
        '''Get depth or specified market. Both asks and bids are sorted from highest price to lowest.

        :param market: Unique market id
        :param limit: (optional) Limit the number of returned price levels
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        return self.__public_request('GET', 'depth', kwargs)

    def get_trades(self, market, **kwargs):
        '''Get recent trades on market, each trade is included only once.

        :param market: Unique market id
        :param limit: (optional) Limit the number of returned trades
        :param timestamp: (optional) An integer represents the seconds elapsed since Unix epoch
        :param from_id: (optional) Trade id
        :param to: (optional) Trade id
        :param order_by: (optional) If set, returned trades will be sorted in specific order
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        if kwargs['from_id'] is not None:
            kwargs['from'] = kwargs['from_id']
            kwargs.pop('from_id')
        return self.__public_request('GET', 'trades', kwargs)

    def get_trades_my(self, market, **kwargs):
        '''Get your executed trades. Trades are sorted in reverse creation order.

        :param market: Unique market id
        :param limit: (optional) Limit the number of returned trades
        :param timestamp: (optional) An integer represents the seconds elapsed since Unix epoch
        :param from_id: (optional) Trade id
        :param to: (optional) Trade id
        :param order_by: (optional) If set, returned trades will be sorted in specific order
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        if kwargs['from_id'] is not None:
            kwargs['from'] = kwargs['from_id']
            kwargs.pop('from_id')
        return self.__private_request('GET', 'trades/my', kwargs)

    def get_timestamp(self):
        '''Get server current time, in seconds since Unix epoch.

        :return: :class:`dict`
        '''
        return self.__public_request('GET', 'timestamp')

    def get_k(self, market, **kwargs):
        '''Get OHLC(k line) of specific market.

        :param market: Unique market id
        :param limit: (optional) Limit the number of returned data points
        :param period: (optional) Time period of K line
        :param timestamp: (optional) An integer represents the seconds elapsed since Unix epoch
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        return self.__public_request('GET', 'k', kwargs)

    def get_order(self, id):
        '''Get information of specified order.

        :param id: Unique order id
        :return: :class:`dict`
        '''
        return self.__private_request('GET', 'order', {
            'id': id
        })

    def post_order_delete(self, id):
        '''Cancel an order.

        :param id: Unique order id
        :return: :class:`dict`
        '''
        return self.__private_request('POST', 'order/delete', {
            'id': id
        })

    def get_k_with_pending_trades(self, market, trade_id, **kwargs):
        '''Get K data with pending trades

        :param market: Unique market id
        :param trade_id: The trade id of the first trade you received
        :param limit: (optional) Limit the number of returned data points
        :param period: (optional) Time period of K line
        :param timestamp: (optional) An integer represents the seconds elapsed since Unix epoch
        :return: :class:`dict`
        '''
        kwargs['market'] = market
        kwargs['trade_id'] = trade_id
        return self.__public_request('GET', 'k_with_pending_trades', kwargs)

    def get_addresses_address(self, address):
        '''Check Deposit Address.

        :param address:
        :return: :class:`dict`
        '''
        return self.__public_request('GET', 'addresses/' + address)

    def get_partners_orders_id_trades(self, id, access_key_hash):
        '''

        :param id:
        :param access_key_hash:
        :return: :class:`dict`
        '''
        return self.__public_request('GET', 'partners/orders/' + id + 'trades', {
            'access_key_hash': access_key_hash
        })
