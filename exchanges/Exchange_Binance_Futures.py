from exchanges.Exchange_class import Exchange
from binance_futures.client import as Futures_Client
from datetime import datetime
from time import sleep
import pandas as pd
from binance.client import Client as Spot_Client
# from binance import Client as Spot_Client

class Exchange_Binance_Spot(Exchange):
    def __init__(self, kwargs):
        super(Exchange_Binance_Spot, self).__init__(bot=kwargs)
        self.min_leverage = 1
        self.max_leverage = 1
        self.default_leverage = 1
        self.secret_key = "Add Binance Spot Secret Here"
        self.api_key = "Add Binance API Key Here"
        self.taker_fee = 0.0004
        self.maker_fee = 0.0001
        self.live = False
        self.can_short = False

    def initialise(self):
        self.client = Spot_Client(self.api_key, self.secret_key)

    def get_account_balance(self,symbol='USDT'):
        assets = self.client.get_account()
        for asset in assets:
            if asset["asset"] == symbol:
                result = asset
        return float(result["balance"])

    # def get_futures_position(self, instrument):
    #     assets = self.client.futures_position_information(symbol=instrument)
    #     return float(assets[0]["positionAmt"])

    # def get_futures_ticker(self, instrument):
    #     result = self.client.futures_symbol_ticker(symbol=instrument)
    #     return float(result["price"])

    def futures_create_order(self, symbol, side, type, stopPrice = 0.0, closePosition='', quantity=0.0):
        if type=='STOP_MARKET':
            if (stopPrice == 0.0 or closePosition==''):
                raise Exception('STOP MARKET must have STOP PRICE and CLOSE POSITION')
            else:
                self.client.futures_create_order(symbol=symbol, side=side, type=type, stopPrice = stopPrice, closePosition=closePosition)
                # print('DUMMY ORDER', symbol, side, type, stopPrice, closePosition)

        elif (type=="MARKET"):
            if quantity==0.0:
                raise Exception('BUY and SELL order require quantity')
            else:
                self.client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
                # print('DUMMY ORDER', symbol, side, type, quantity=quantity)

    def get_excel_data(self, fname):
        return pd.read_excel(fname)

    def get_klines(self, symbol, interval, start_time=None, end_time=None, limit=1000, utc=False, date_split=False):
        self.source='binance'
        if date_split:
            end_time=int(datetime(2020,9,30,0,0).timestamp()*1000)
        if self.source=='binance':
            self.client = Spot_Client(self.api_key, self.secret_key)
            count = 0
            max_increment = 1000
            loop_done = False
            all_results = []
            while not loop_done:
                if count + max_increment > limit:
                    get_next = limit - count + 1
                    loop_done=True

                else:
                    get_next = max_increment
                sleep(1)
                # result = self.client.futures_klines(symbol=symbol, interval=interval, endTime=end_time, limit=get_next)
                result = self.client.get_historical_klines(symbol=symbol, interval=interval, endTime=end_time, limit=get_next)
                all_results = result[:-1] + all_results
                count += get_next -1
                end_time = result[0][0]
                sleep(1)
            temp_list = []
            if interval in ['1m', '3m', '5m', '15m', '30m']:
                start_pos = 3
                end_pos = 16
            else:
                start_pos = 3
                end_pos = 13
            for cs in all_results:
                if utc:
                    str_datetime = str(datetime.fromtimestamp(cs[0] / 1000, tz=pytz.utc))
                else:
                    str_datetime = str(datetime.fromtimestamp(cs[0] / 1000))
                temp_list.append([str_datetime, str_datetime[start_pos:end_pos], float(cs[1]), float(cs[2]), float(cs[3]), float(cs[4])])
            try:
                del self.df
            except:
                pass
            self.df = pd.DataFrame(temp_list)
            self.df.columns = ['date_time', 'short_date_time', 'open', 'high', 'low', 'close']
            return self.df

class Exchange_Binance_Futures(Exchange):
    def __init__(self, kwargs):
        super(Exchange_Binance_Futures, self).__init__(bot=kwargs)
        self.min_leverage = 1
        self.max_leverage = 125
        self.default_leverage = 20
        self.api_key = "Add Binance Futures API Key Here"
        self.secret_key = "Add Binance Futures Secret Here"
        self.taker_fee = 0.0004
        self.maker_fee = 0.0001
        self.live = False
        self.can_short = True

    def initialise(self):
        self.client = Futures_Client(self.api_key, self.secret_key)

    def get_account_balance(self,symbol='USDT'):
        assets = self.client.futures_account_balance(symbol=symbol)
        for asset in assets:
            if asset["asset"] == "USDT":
                result = asset
        return float(result["balance"])

    def get_futures_position(self, instrument):
        assets = self.client.futures_position_information(symbol=instrument)
        return float(assets[0]["positionAmt"])

    def get_futures_ticker(self, instrument):
        result = self.client.futures_symbol_ticker(symbol=instrument)
        return float(result["price"])

    def futures_create_order(self, symbol, side, type, stopPrice = 0.0, closePosition='', quantity=0.0):
        if type=='STOP_MARKET':
            if (stopPrice == 0.0 or closePosition==''):
                raise Exception('STOP MARKET must have STOP PRICE and CLOSE POSITION')
            else:
                self.client.futures_create_order(symbol=symbol, side=side, type=type, stopPrice = stopPrice, closePosition=closePosition)
                # print('DUMMY ORDER', symbol, side, type, stopPrice, closePosition)

        elif (type=="MARKET"):
            if quantity==0.0:
                raise Exception('BUY and SELL order require quantity')
            else:
                self.client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
                # print('DUMMY ORDER', symbol, side, type, quantity=quantity)

    def get_excel_data(self, fname):
        return pd.read_excel(fname)

    def get_klines(self, symbol, interval, start_time=None, end_time=None, limit=1000, utc=False, date_split=False):
        self.source='binance'
        if date_split:
            end_time=int(datetime(2020,9,30,0,0).timestamp()*1000)
        if self.source=='binance':
            self.client = Futures_Client(self.api_key, self.secret_key)
            count = 0
            max_increment = 1000
            loop_done = False
            all_results = []
            while not loop_done:
                if count + max_increment > limit:
                    get_next = limit - count + 1
                    loop_done=True

                else:
                    get_next = max_increment
                sleep(1)
                result = self.client.futures_klines(symbol=symbol, interval=interval, endTime=end_time, limit=get_next)
                all_results = result[:-1] + all_results
                count += get_next -1
                end_time = result[0][0]
                sleep(1)
            temp_list = []
            if interval in ['1m', '3m', '5m', '15m', '30m']:
                start_pos = 3
                end_pos = 16
            else:
                start_pos = 3
                end_pos = 13
            for cs in all_results:
                if utc:
                    str_datetime = str(datetime.fromtimestamp(cs[0] / 1000, tz=pytz.utc))
                else:
                    str_datetime = str(datetime.fromtimestamp(cs[0] / 1000))
                temp_list.append([str_datetime, str_datetime[start_pos:end_pos], float(cs[1]), float(cs[2]), float(cs[3]), float(cs[4])])
            try:
                del self.df
            except:
                pass
            self.df = pd.DataFrame(temp_list)
            self.df.columns = ['date_time', 'short_date_time', 'open', 'high', 'low', 'close']
            return self.df


