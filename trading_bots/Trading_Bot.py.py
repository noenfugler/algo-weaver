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
from strategies.Strategies import *
from instruments.Instruments import *
from exchanges.Exchange_Binance import Exchange_Binance_Spot
from exchanges.Exchange_Binance import Exchange_Binance_Futures
from datasets.Datasets import *
from indicators.Indicators import *
from utils.util_functions import *
from datetime import datetime, timedelta
from time import sleep


class Backtest_CCI(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_CCI, self).__init__(kwargs)
        else:
            super(Backtest_CCI, self).__init__()


    def initialise(self, **kwargs):

        self.starting_cash=0
        self.trading_cash=0
        self.starting_position=1
        self.position = 1
        self.maximum_allocation=0.1

        # self.exchange = Exchange_Binance_Spot(self)
        self.exchange = Exchange_Binance_Futures(self)
        self.exchange.initialise()


        # self.strategy =  Strategy_CCI_re_im_cross_long_only(silent=False, allow_long=True, allow_short=False, bot=self)
        # self.strategy = Strategy_CCI_period_imag_and_mama(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_imag(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_real(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_real_and_mama(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_imag_and_mama(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_imag(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_re_im_cross(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_re_im_range(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_cycle_only(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_period_trend_only(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        # self.strategy = Strategy_CCI_gap_and_mama(silent=False, allow_long=True, allow_short=False, bot=self)
        self.strategy = Strategy_pc_fama_cross_zero(silent=False, allow_long=True, allow_short=False, bot=self)
        self.strategy = Strategy_pc_fama_peak_trough(silent=False, allow_long=True, allow_short=False, bot=self)

        self.instrument = Instrument_BTCUSDT()
        # self.instrument = Instrument_ETHUSDT()
        # self.instrument = Instrument_BCHUSDT()
        # self.instrument = Instrument_ETHBTC()

        # timeframe=('1m',1, False)
        # timeframe=('5m',5, False)
        # timeframe=('15m',15, False)
        # timeframe=('1h',60, True)
        timeframe=('1d',60, True)
        # timeframe=('1w',60, True)

        # self.interval = '15m'
        self.interval = timeframe[0]
        # self.interval = '1h'

        self.live=False

        indicator1 = Indicator_Super_Smoother()
        self.ls_indicators.append(indicator1)

        indicator2 = Indicator_CCI()
        self.ls_indicators.append(indicator2)

        indicator3 = Indicator_I1_Q1()
        self.ls_indicators.append(indicator3)

        indicator4 = Indicator_MAMA()
        self.ls_indicators.append(indicator4)

        indicator5 = Indicator_Ehlers_Period()
        self.ls_indicators.append(indicator5)

        indicator6 = Indicator_price()
        self.ls_indicators.append(indicator6)

        indicator7 = Indicator_Detrender()
        self.ls_indicators.append(indicator7)

        indicator8 = Indicator_percent_change()
        self.ls_indicators.append(indicator8)

        indicator9 = Indicator_Super_Smoother()
        self.ls_indicators.append(indicator9)

        # indicator10 = Indicator_Trend_AJ()
        # self.ls_indicators.append(indicator10)
        #
        indicator11 = Indicator_Super_Smoother()
        self.ls_indicators.append(indicator11)


        self.dataset = Dataset_Binance_Futures_1h_100_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)
        self.dataset.load_data()

        indicator1.create(self.dataset.data, source='close', destination='ss_close')
        indicator2.create(self.dataset.data, source='close')
        indicator3.create(self.dataset.data,source='cci_real', period='cci_period')
        indicator4.create(self.dataset.data,ss_period=10)
        indicator5.create(self.dataset.data, source1='mama', source_re='cci_real', source_im='cci_imag')
        indicator6.create(self.dataset.data)
        indicator7.create(self.dataset.data, source='price')
        indicator8.create(self.dataset.data, source='ss_fama', destination='pc_fama')
        indicator9.create(self.dataset.data, source='detrender', destination='ss_detrender', ss_period=2)
        # indicator10.create(self.dataset.data)
        indicator11.create(self.dataset.data, source='pc_fama', destination='ss_pc_fama', ss_period=5)

last_run = datetime.now()
time_gap = 60
first_run = True
interval = timedelta(minutes=time_gap)

while True:
    if (datetime.now() >= last_run + interval) or first_run:
        first_run = False
        last_run = datetime.now()
        last_run = round_time(last_run,timedelta(minutes=time_gap), to='down')
        try:
            del my_backtest
        except:
            pass
        sleep(10)
        my_backtest = Backtest_CCI()
        my_backtest.initialise()
        my_backtest.run()
        my_backtest.report()
        my_backtest.strategy.graph()
        print(last_run)
#git test
        # exit()
