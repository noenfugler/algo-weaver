#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from backtests.Backtest_class import Backtest
from strategies.strategy_CCI_state_and_re_im_long_only import Strategy_CCI_state_and_re_im_long_only
from strategies.strategy_CCI_imag_and_mama_long_only import Strategy_CCI_imag_and_mama_long_only
from strategies.strategy_CCI_period_imag_and_mama_long_only import Strategy_CCI_period_imag_and_mama_long_only
from strategies.strategy_CCI_period_imag_and_mama_long_short import Strategy_CCI_period_imag_and_mama_long_short
# from instruments.Instrument_BTCAUD import Instrument_BTCAUD
from instruments.Instrument_BTCUSDT import Instrument_BTCUSDT
# import instruments.Instruments as I
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


        self.strategy = Strategy_CCI_period_imag_and_mama_long_only(silent=False, trade_short=False, bot=self)

        self.instrument = Instrument_BTCUSDT()

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
        indicator4.create(self.dataset.data,ss_period=8)
        self.ls_indicators.append(indicator4)

    def graph(self):
        self.data_active = self.data #.iloc[self.get_warmup_candles():]
        fig, axs = plt.subplots(3, figsize=(15, 9.5))
        fig.suptitle(self.interval + ' CCI BTCAUD' + str(self.data_active['date_time'].tail(1).values[0][:19]))
        axs[0].set_yscale('log')
        # axs[0].set_ylim(50000,80000)
        line1 = axs[0].plot(self.data_active['date_time'], self.data_active['close'],color='black', linewidth=0.75)
        line1 = axs[0].plot(self.data_active['date_time'], self.data_active['ss_mama'],color='green', linewidth=0.75)

        axs2=axs[0].twinx()
        line1 = axs2.plot(self.data['date_time'], self.data['cci_mode_aj'],color='purple', linewidth=0.75)
        line4 = axs[1].plot(self.data_active['date_time'], self.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.data_active['date_time'], self.data_active['cci_real'],color='blue', linewidth=0.75)
        axs[2].set_ylim(0,50)
        line = axs[2].plot(self.data_active['date_time'], self.data_active['cci_period_aj'],color='red', linewidth=0.75)

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs[0].plot(buy_x, buy_y, '^', color='blue', markersize=7)
        axs[0].plot(sell_x, sell_y, 'v', color='red', markersize=7)

        plt.show()

    def graph_single(self):
        fig, axs = plt.subplots(1, figsize=(15, 9.5))
        fig.suptitle(self.interval + ' CCI BTCAUD' + str(self.data['date_time'].tail(1).values[0][:19]))
        axs.set_yscale('log')
        line1 = axs.plot(self.data['date_time'], self.data['close'],color='black', linewidth=0.75)
        line1 = axs.plot(self.data['date_time'], self.data['ss_mama'],color='green', linewidth=0.75)
        # line2 = axs[1].plot(self.data['date_time'], self.data['cci_angle'],color='black', linewidth=0.75)
        # line3 = axs[1].plot(self.data['date_time'], self.data['cci_state'],color='blue', linewidth=0.75)
        axs2=axs.twinx()
        line4 = axs2.plot(self.data['date_time'], self.data['cci_imag'],color='red', linewidth=0.75)
        line5 = axs2.plot(self.data['date_time'], self.data['cci_real'],color='blue', linewidth=0.75)
        # axs[1].set_yscale('log')
        # line4 = axs[1].plot(self.data['date_time'], self.data['cci_period'],color='green', linewidth=0.75)
        # axs3 = axs[1].twinx()
        # line4 = axs3.plot(self.data['date_time'], self.data['cci_angle_roc'],color='black', linewidth=0.75)

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs.plot(buy_x, buy_y, '^', color='blue', markersize=7)
        axs.plot(sell_x, sell_y, 'v', color='red', markersize=7)

        plt.show()




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
        my_backtest.graph()
        # my_backtest.graph_single()
        sleep(1)
