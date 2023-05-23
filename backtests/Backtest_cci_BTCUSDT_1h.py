#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from backtests.Backtest_class import Backtest
from strategies.strategy_CCI_state_and_re_im_long_only import Strategy_CCI_state_and_re_im_long_only
from strategies.strategy_CCI_imag_and_mama_long_only import Strategy_CCI_imag_and_mama_long_only
from strategies.strategy_CCI_period_imag_and_mama_long_only import Strategy_CCI_period_imag_and_mama_long_only
from strategies.strategy_CCI_period_imag_and_mama import Strategy_CCI_imag_and_mama
from strategies.strategy_CCI_period_imag_and_mama_long_short import Strategy_CCI_period_imag_and_mama_long_short
from instruments.Instruments import *
from exchanges.Exchange_Binance import Exchange_Binance_Spot
from exchanges.Exchange_Binance import Exchange_Binance_Futures
from datasets.Binance_Spot_1h_1000_candles import Dataset_Binance_Spot_1h_1000_candles
from datasets.Binance_Spot_1h_100_candles import Dataset_Binance_Spot_1h_100_candles
from datasets.Binance_Futures_1h_100_candles import Dataset_Binance_Futures_1h_100_candles
from datasets.Binance_Futures_1h_250_candles import Dataset_Binance_Futures_1h_250_candles
from indicators.Indicator_MAMA import Indicator_MAMA
from indicators.Indicator_I1_Q1 import Indicator_I1_Q1
from indicators.Indicator_CCI import Indicator_CCI
from indicators.Indicator_Super_Smoother import Indicator_Super_Smoother
import matplotlib.pyplot as plt
from datetime import datetime
from time import sleep


class Backtest_CCI_AUDUSDT_1h(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_CCI_AUDUSDT_1h, self).__init__(kwargs)
        else:
            super(Backtest_CCI_AUDUSDT_1h, self).__init__()


    def initialise(self, **kwargs):

        self.starting_cash=0
        self.trading_cash=0
        self.starting_position=1
        self.position = 1

        # self.exchange = Exchange_Binance_Spot(self)
        self.exchange = Exchange_Binance_Futures(self)
        self.exchange.initialise()


        self.strategy = Strategy_CCI_imag_and_mama(silent=False, allow_long=True, allow_short=False, bot=self)

        # self.instrument = Instrument_BTCUSDT()
        self.instrument = Instrument_ETHUSDT()
        # self.instrument = Instrument_BCHUSDT()
        # self.instrument = Instrument_ETHBTC()
        #
        # self.interval = '15m'
        self.interval = '1h'

        self.live=False

        self.dataset = Dataset_Binance_Futures_1h_250_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)
        self.dataset.load_data()

        indicator1 = Indicator_Super_Smoother()
        indicator1.create(self.dataset.data, source='close', destination='ss_close')
        self.ls_indicators.append(indicator1)

        indicator2 = Indicator_CCI()
        # indicator2.create(self.dataset.data, source='ss_close')
        indicator2.create(self.dataset.data, source='close')
        self.ls_indicators.append(indicator2)

        indicator3 = Indicator_I1_Q1()
        indicator3.create(self.dataset.data,source='cci_real', period='cci_period')
        self.ls_indicators.append(indicator3)

        indicator4 = Indicator_MAMA()
        indicator4.create(self.dataset.data,ss_period=4)
        self.ls_indicators.append(indicator4)


my_backtest = Backtest_CCI_AUDUSDT_1h()
last_min = datetime.now().minute
first_run = True

while True:
    if (last_min != datetime.now().minute and datetime.now().minute % 60 == 0) or first_run:
        first_run = False
        last_min = datetime.now().minute
        my_backtest.initialise()
        my_backtest.run()
        my_backtest.report()
        my_backtest.strategy.graph()
        # my_backtest.graph_single()
        sleep(1)
        exit()
