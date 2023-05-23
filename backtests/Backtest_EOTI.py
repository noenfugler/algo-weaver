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
from graphs.Graphs import *
from communicators.telegram_communicator import *
from indicators.Indicators import *
from utils.util_functions import *
from configs.Config_class import *
from datetime import datetime, timedelta
from time import sleep


class Backtest_EOTI(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_EOTI, self).__init__(**kwargs)
        else:
            super(Backtest_EOTI, self).__init__()

    def graph(self, save):
        my_graph = Graph_Early_Onset_Trend(strategy=self.strategy, save=save)
        image = my_graph.graph()
        return image

    def initialise(self, **kwargs):

        self.starting_cash=0
        self.trading_cash=0
        self.starting_position=1
        self.position = 1
        self.maximum_allocation=0.1

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
        # self.strategy = Strategy_pc_fama_cross_zero(silent=False, allow_long=True, allow_short=False, bot=self)
        # self.strategy = Strategy_pc_fama_peak_trough(silent=False, allow_long=True, allow_short=False, bot=self)
        # self.strategy = Strategy_mama_fama_cross(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)
        self.strategy = Strategy_early_onset_trend_indicator(silent=False,allow_long=True, allow_short=False, bot=self)

        self.live=False

        indicator1 = Indicator_Ehlers_Early_Onset_Trend()
        self.ls_indicators.append(indicator1)


        self.dataset = Dataset_Binance_Futures_1h_100_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)
        self.dataset.load_data()

        indicator1.create(self.dataset.data)

def main():

    use_telegram=False
    config1 = Config(instrument=Instrument_BTCAUD(), interval='1h', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config1 = Config(instrument=Instrument_BTCAUD(), interval='15m', wait_time=15, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config1 = Config(instrument=Instrument_BTCAUD(), interval='15', wait_time=5, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config1 = Config(instrument=Instrument_BTCAUD(), interval='1m', wait_time=1, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    config2 = Config(instrument=Instrument_ETHAUD(), interval='1h', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config2 = Config(instrument=Instrument_ETHAUD(), interval='15m', wait_time=15, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config2 = Config(instrument=Instrument_ETHAUD(), interval='15', wait_time=5, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config2 = Config(instrument=Instrument_ETHAUD(), interval='1m', wait_time=1, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    config3 = Config(instrument=Instrument_ETHBTC(), interval='1h', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config3 = Config(instrument=Instrument_ETHAUD(), interval='15m', wait_time=15, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config3 = Config(instrument=Instrument_ETHAUD(), interval='15', wait_time=5, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config3 = Config(instrument=Instrument_ETHAUD(), interval='1m', wait_time=1, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    # self.exchange = Exchange_Binance_Spot(self)
    # self.exchange = Exchange_Binance_Futures(self)

    last_run = datetime.now()
    first_run = True
    wait_time = timedelta(minutes=config1.wait_time)
    my_telegram = Telegram_Communicator()
    my_backtest1 = Backtest_EOTI(instrument=config1.instrument, interval=config1.interval, exchange=config1.exchange)
    my_backtest2 = Backtest_EOTI(instrument=config2.instrument, interval=config2.interval, exchange=config2.exchange)
    my_backtest3 = Backtest_EOTI(instrument=config3.instrument, interval=config3.interval, exchange=config3.exchange)

    while True:
        if (datetime.now() >= last_run + wait_time) or first_run:
            first_run = False
            last_run = datetime.now()
            last_run = round_time(last_run,timedelta(minutes=config1.wait_time), to='down')


            #run backtest with first config

            my_backtest1.initialise()
            my_backtest1.run()
            my_backtest1.report()

            image = my_backtest1.graph(config1.use_telegram)
            if config1.use_telegram:
                done=False
                fail_count=0
                while not done:
                    try:
                        my_telegram.send_graph(image)
                        done=True
                        print('Sent to Telegram.')
                    except:
                        print('Sending failed.')
                        fail_count+=1
                        sleep(2^fail_count)
                        if fail_count > 9:
                            done=True


            # run backtest with second config

            my_backtest2.initialise()
            my_backtest2.run()
            my_backtest2.report()

            image = my_backtest2.graph(config2.use_telegram)
            if config2.use_telegram:
                done = False
                fail_count = 0
                while not done:
                    try:
                        my_telegram.send_graph(image)
                        done = True
                    except:
                        print('Sending failed.')
                        fail_count += 1
                        sleep(2 ^ fail_count)
                        if fail_count > 9:
                            done = True

            # run backtest with THIRD config

            my_backtest3.initialise()
            my_backtest3.run()
            my_backtest3.report()

            image = my_backtest3.graph(config3.use_telegram)
            if config3.use_telegram:
                done=False
                fail_count=0
                while not done:
                    try:
                        my_telegram.send_graph(image)
                        done=True
                        print('Sent to Telegram.')
                    except:
                        print('Sending failed.')
                        fail_count+=1
                        sleep(2^fail_count)
                        if fail_count > 9:
                            done=True


            # my_graph2 = CCI_PC_fama_graph(strategy=my_backtest2.strategy)
            # my_graph = CCI_fama_predictor_graph(strategy=my_backtest.strategy)

            exit()
        sleep(1)


if __name__ == "__main__":
    main()
