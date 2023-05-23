from backtests.Backtest_class import Backtest
from strategies.strategy_CCI_state_and_angle_long_only import Strategy_CCI_state_and_angle_long_only
from strategies.strategy_cci_imag_long_only import Strategy_CCI_imag_long_only
from strategies.strategy_cci_re_im_cross import Strategy_CCI_re_im_cross_long_only
from instruments.Instrument_ETHBTC import Instrument_ETHBTC
from exchanges.Exchange_Binance import Exchange_Binance_Spot
from datasets.Binance_Spot_ETHBTC_1h_250_candles import Dataset_Binance_Spot_ETHBTC_1h_250_candles
from indicators.Indicator_CCI import Indicator_CCI
import matplotlib.pyplot as plt
import numpy as np


class Backtest_CCI_ETHBTC_1h(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_CCI_ETHBTC_1h, self).__init__(kwargs)
        else:
            super(Backtest_CCI_ETHBTC_1h, self).__init__()


    def initialise(self, **kwargs):

        self.starting_cash=0
        self.trading_cash=0
        self.starting_position=1
        self.position = 1

        self.exchange = Exchange_Binance_Spot(self)
        self.exchange.initialise()


        self.strategy = Strategy_CCI_state_and_angle_long_only(silent=False, trade_short=False, bot=self)

        self.instrument = Instrument_ETHBTC()

        self.interval = '1h'

        self.live=False

        self.dataset = Dataset_Binance_Spot_ETHBTC_1h_250_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)
        self.dataset.load_data()
        indicator = Indicator_CCI()
        indicator.create(self.dataset.data)
        self.ls_indicators.append(indicator)
        # self.create_indicators()


    def graph(self):
        fig, axs = plt.subplots(2, figsize=(15, 9.5))
        fig.suptitle(self.interval + ' CCI ETHBTC' + str(self.data['date_time'].tail(1).values[0][:19]))
        line1 = axs[0].plot(self.data['date_time'], self.data['close'],color='black', linewidth=0.75)
        # line2 = axs[1].plot(self.data['date_time'], self.data['cci_angle'],color='black', linewidth=0.75)
        # line3 = axs[1].plot(self.data['date_time'], self.data['cci_state'],color='blue', linewidth=0.75)
        axs2=axs[0].twinx()
        line4 = axs2.plot(self.data['date_time'], self.data['cci_imag'],color='red', linewidth=0.75)
        line5 = axs2.plot(self.data['date_time'], self.data['cci_real'],color='blue', linewidth=0.75)
        axs[1].set_yscale('log')
        # line4 = axs[1].plot(self.data['date_time'], self.data['cci_period'],color='green', linewidth=0.75)
        axs3 = axs[1].twinx()
        line4 = axs3.plot(self.data['date_time'], self.data['cci_angle_roc'],color='black', linewidth=0.75)

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

my_backtest = Backtest_CCI_ETHBTC_1h()
my_backtest.initialise()
my_backtest.run()
my_backtest.report()
my_backtest.graph()
