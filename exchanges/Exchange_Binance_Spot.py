#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from exchanges.Exchange_class import Exchange
from datetime import datetime
from time import sleep
import pandas as pd
from binance.client import Client as Spot_Client
from exchanges import Exchange_Binance_Spot_Secrets
# from binance import Client as Spot_Client

class Exchange_Binance_Spot(Exchange):
    def __init__(self, **kwargs):
        super(Exchange_Binance_Spot, self).__init__()
        self.min_leverage = 1
        self.max_leverage = 1
        self.default_leverage = 1
        # Secret Key and API Key should be defined in a file called Exchange_{NAME}_Secrets.py
        self.secret_key = Exchange_Binance_Spot_Secrets.secret_key
        self.api_key = Exchange_Binance_Spot_Secrets.api_key
        self.taker_fee = 0.0001
        self.maker_fee = 0.0001
        self.live = False
        self.can_short = False

    def initialise(self):
        self.client = Spot_Client(self.api_key, self.secret_key)

    def get_account_balance(self,symbol=''):
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
            all_results = self.client.get_historical_klines(symbol=symbol, interval=interval, end_str=end_time, start_str= start_time, limit=limit)
                # all_results = result[:-1] + all_results
                # count += get_next -1
                # end_time = result[0][0]
                # sleep(1)
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
