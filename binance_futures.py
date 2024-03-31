import datetime

import time


import requests




class BinanceFutures:
    def __init__(self, public_key, secret_key):

        self.base_url = "https://testnet.binancefuture.com"
        self.public_key = public_key
        self.secret_key = secret_key
        self.headers = {'X-MBX-APIKEY': self.public_key}# needs an extra header acording to the docs





    def make_request(self, method, endpoint, data):
        if method == "GET":
            response = requests.get(self.base_url + endpoint, params=data, headers=self.headers)#makes request to "https://testnet.binancefuture.com"
        else:
            print("This method not yet supported")

        if response.status_code == 200:
            return response.json()#converts json data into a dictionary
        else:
            print(f"Error in {method} request to {endpoint}: {response.json()} (error code {response.status_code})")
            return None



    def get_candles(self, symbol, interval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = 1000

        response = self.make_request("GET", "/fapi/v1/klines", data)

        candles = []

        if response is not None:
            for i in response:
                date_time = i[0]
                base_datetime = datetime.datetime(1970, 1, 1)
                delta = datetime.timedelta(0, 0, 0, date_time)
                date_time = base_datetime + delta
                candles.append([date_time, float(i[1])])#appends the candles array with the now modified date and the open price of the symbol

        return candles




    def getPrice(self, symbol):
        data = dict()
        data['symbol'] = symbol
        prices = self.make_request("GET", "/fapi/v1/ticker/price", data)
        return prices





