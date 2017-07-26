#!/usr/bin/env python3

import hmac
import requests
import time
from hashlib import sha256

BASE_URL = 'https://yunbi.com/api/v2/'


class Yunbi():
    def __init__(self, access_key=None, secret_key=None):
        if access_key == None and secret_key == None:
            self.auth = False
        else:
            self.auth = True
            self.access_key = access_key
            self.secret_key = secret_key

    def __hmac_sha256(self, key, msg):
        hash_obj = hmac.new(key=key, msg=msg, digestmod=sha256)
        return hash_obj.hexdigest()

    def __sign(self, method, url, params):
        message = '%s|/api/v2/%s.json|' % (method, url)
        for i in sorted(params.items()):
            message += '%s=%s&' % (i[0], i[1])
        return self.__hmac_sha256(self.secret_key.encode(), message[:-1].encode())

    def __public_request(self, method, url, data=None):
        assert method in ['GET', 'POST'], 'Unknow method %s' % method
        data = {} if data is None else data
        if method == 'GET':
            return requests.get(BASE_URL + url + '.json', data=data).json()
        else:
            return requests.post(BASE_URL + url + '.json', data=data).json()

    def __private_request(self, method, url, data=None):
        assert method in ['GET', 'POST'], 'Unknow method %s' % method
        assert self.auth == True, 'Private API, access_key and secret_key required'
        data = {} if data is None else data
        data['access_key'] = self.access_key
        tonce = int(time.time() * 1000)
        data['tonce'] = tonce
        signature = self.__sign(method, url, data)
        data['signature'] = signature
        if method == 'GET':
            return requests.get(BASE_URL + url + '.json', data=data).json()
        else:
            return requests.post(BASE_URL + url + '.json', data=data).json()

    def get_markets(self):
        return self.__public_request('GET', 'markets')

    def get_tickers(self):
        return self.__public_request('GET', 'tickers')

    def get_tickets_market(self, market):
        return self.__public_request('GET', 'tickers/' + market)

    def get_members_me(self):
        return self.__private_request('GET', 'members/me')

    def get_deposits(self, **kwargs):
        return self.__private_request('GET', 'deposits', kwargs)

    def get_deposit(self, txid):
        return self.__private_request('GET', 'deposit', {
            'txid': txid
        })

    def get_orders(self, market, **kwargs):
        kwargs['market'] = market
        return self.__private_request('GET', 'orders', kwargs)

    def post_orders(self, market, side, volume, **kwargs):
        kwargs['market'] = market
        kwargs['side'] = side
        kwargs['volume'] = volume
        return self.__private_request('POST', 'orders', kwargs)

    def post_orders_multi(self, market, orders):
        return self.__private_request('POST', 'orders/multi', {
            'market': market,
            'orders': orders
        })

    def post_orders_clear(self, **kwargs):
        return self.__private_request('POST', 'orders/clear', kwargs)

    def get_deposit_address(self, currency):
        return self.__private_request('GET', 'deposit_address', {
            'currency': currency
        })

    def get_order_book(self, market, **kwargs):
        kwargs['market'] = market
        return self.__public_request('GET', 'order_book', kwargs)

    def get_depth(self, market, **kwargs):
        kwargs['market'] = market
        return self.__public_request('GET', 'depth', kwargs)

    def get_trades(self, market, **kwargs):
        kwargs['market'] = market
        return self.__public_request('GET', 'trades', kwargs)

    def get_trades_my(self, market, **kwargs):
        kwargs['market'] = market
        return self.__private_request('GET', 'trades/my', kwargs)

    def get_timestamp(self):
        return self.__public_request('GET', 'timestamp')

    def get_k(self, market, **kwargs):
        kwargs['market'] = market
        return self.__public_request('GET', 'k', kwargs)

    def get_order(self, id):
        return self.__private_request('GET', 'order', {
            'id': id
        })

    def post_order_delete(self, id):
        return self.__private_request('POST', 'order/delete', {
            'id': id
        })

    def get_k_with_pending_trades(self, market, trade_id, **kwargs):
        kwargs['market'] = market
        kwargs['trade_id'] = trade_id
        return self.__public_request('GET', 'k_with_pending_trades', kwargs)

    def get_addresses_address(self, address):
        return self.__public_request('GET', 'addresses/' + address)

    def get_partners_orders_id_trades(self, id, access_key_hash):
        return self.__public_request('GET', 'partners/orders/' + id + 'trades', {
            'access_key_hash': access_key_hash
        })
