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


class Backtest_CCI_suite(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_CCI_suite, self).__init__(**kwargs)
        else:
            super(Backtest_CCI_suite, self).__init__()

    def graph(self, save):
        my_graph = Graph_CCI_suite(strategy=self.strategy, save=save)
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
        self.strategy = Strategy_mama_fama_cross(silent=False, allow_long=True, allow_short=False, bot=self, trend_factor=1.0)


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

        indicator10 = Indicator_CTI()
        self.ls_indicators.append(indicator10)
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
        indicator2.create(self.dataset.data, source='close', period=10)
        indicator3.create(self.dataset.data,source='cci_real', period='cci_period')
        indicator4.create(self.dataset.data,ss_period=10)
        indicator5.create(self.dataset.data, source1='mama', source_re='cci_real', source_im='cci_imag')
        indicator6.create(self.dataset.data)
        indicator7.create(self.dataset.data, source='price')
        indicator8.create(self.dataset.data, source='ss_fama', destination='pc_fama')
        indicator9.create(self.dataset.data, source='detrender', destination='ss_detrender', ss_period=2)
        indicator10.create(self.dataset.data, speriod=12, lperiod=36)
        indicator11.create(self.dataset.data, source='pc_fama', destination='ss_pc_fama', ss_period=5)


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
    my_backtest1 = Backtest_mama_fama_cross(instrument=config1.instrument, interval=config1.interval, exchange=config1.exchange)
    my_backtest2 = Backtest_mama_fama_cross(instrument=config2.instrument, interval=config2.interval, exchange=config2.exchange)
    my_backtest3 = Backtest_mama_fama_cross(instrument=config3.instrument, interval=config3.interval, exchange=config3.exchange)

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
