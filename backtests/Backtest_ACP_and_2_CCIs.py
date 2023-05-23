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


class Backtest_ACP_and_2_CCIs(Backtest):
    def __init__(self, **kwargs):
        super(Backtest_ACP_and_2_CCIs, self).__init__(**kwargs)
        self.acp_max=kwargs['acp_max']

    def graph(self, save):
        my_graph = Graph_ACP_and_2_CCIs(strategy=self.strategy, save=save,acp_max=self.acp_max)
        image=my_graph.graph()
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
        # self.strategy = Strategy_early_onset_trend_indicator(silent=False,allow_long=True, allow_short=False, bot=self)
        # self.strategy = Strategy_Do_Nothing(silent=False,allow_long=True, allow_short=False, bot=self)
        self.strategy = Strategy_ACP_and_2_CCIs(silent=False,allow_long=True, allow_short=False, bot=self)

        self.live=False

        # indicator1 = Indicator_Ehlers_Early_Onset_Trend()
        # self.ls_indicators.append(indicator1)

        indicator_cci = Indicator_CCI()
        self.ls_indicators.append(indicator_cci)

        indicator_i1_q1 = Indicator_I1_Q1()
        self.ls_indicators.append(indicator_i1_q1)

        indicator_mama = Indicator_MAMA()
        self.ls_indicators.append(indicator_mama)

        indicator_acp = Indicator_ACP()
        self.ls_indicators.append(indicator_acp)

        indicator_ccia_full = Indicator_CCI_Adaptive()
        self.ls_indicators.append(indicator_ccia_full)

        indicator_ccia_half = Indicator_CCI_Adaptive()
        self.ls_indicators.append(indicator_ccia_half)

        indicator_ccia_full = Indicator_CCI_Adaptive()
        self.ls_indicators.append(indicator_ccia_full)

        # self.dataset = Dataset_Binance_Spot_250_candles(exchange=self.exchange, \
        #                                                               live=False, \
        #                                                               interval=self.interval, \
        #                                                               warmup_candles=self.get_warmup_candles(), \
        #                                                               instrument = self.instrument)

        self.dataset = Dataset_Binance_Spot_100_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)

        # self.dataset = Dataset_Binance_Futures_1h_250_candles(exchange=self.exchange, \
        #                                                               live=False, \
        #                                                               interval=self.interval, \
        #                                                               warmup_candles=self.get_warmup_candles(), \
        #                                                               instrument = self.instrument)
        # self.dataset = Dataset_Sine_Wave_100_Candles(exchange=self.exchange, \
        #                                                               live=False, \
        #                                                               interval=self.interval, \
        #                                                               warmup_candles=self.get_warmup_candles(), \
        #                                                               instrument = self.instrument)

        # self.dataset.load_data(period=10., long_period = 42., amplitude_short=1., amplitude_long=0)
        self.dataset.load_data()
        # indicator1.create(self.dataset.data)
        indicator_cci.create(self.dataset.data, source='close')
        indicator_i1_q1.create(self.dataset.data,source='cci_real', period='cci_period')
        indicator_mama.create(self.dataset.data)
        indicator_acp.create(self.dataset.data, avg_length=0, lp_length=10, hp_length=96, acp_max=self.acp_max, source='mama', alpha2=0.4)
        indicator_ccia_half.create(self.dataset.data, source='mama', period='acp_period_half_cycle', mode='highly', destination_prefix='ccia_half')
        indicator_ccia_full.create(self.dataset.data, source='mama', period='acp_period_full_cycle', mode='highly',  destination_prefix='ccia_full')

def main():

    use_telegram=False
    acp_max=int(4*24)
    # config1 = Config(instrument=Instrument_ETHAUD(), interval='1h', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config1 = Config(instrument=Instrument_BTCAUD(), interval='15m', wait_time=15, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config1 = Config(instrument=Instrument_BTCAUD(), interval='5m', wait_time=5, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config1 = Config(instrument=Instrument_BTCAUD(), interval='1m', wait_time=1, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    # config2 = Config(instrument=Instrument_ETHAUD(), interval='1h', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config2 = Config(instrument=Instrument_ETHAUD(), interval='15m', wait_time=15, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config2 = Config(instrument=Instrument_ETHAUD(), interval='15', wait_time=5, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config2 = Config(instrument=Instrument_ETHAUD(), interval='1m', wait_time=1, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    # config3 = Config(instrument=Instrument_ETHBTC(), interval='1h', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    config1 = Config(instrument=Instrument_ETHBTC(), interval='15m', wait_time=15, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config3 = Config(instrument=Instrument_ETHBTC(), interval='15', wait_time=5, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)
    # config3 = Config(instrument=Instrument_ETHBTC(), interval='1m', wait_time=1, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    # self.exchange = Exchange_Binance_Spot(self)
    # self.exchange = Exchange_Binance_Futures(self)

    last_run = datetime.now()
    first_run = True
    wait_time = timedelta(minutes=config1.wait_time)
    my_telegram = Telegram_Communicator()
    my_backtest1 = Backtest_ACP_and_2_CCIs(instrument=config1.instrument, interval=config1.interval, exchange=config1.exchange, acp_max=acp_max)
    drop_last = 18

    while True:
        if (datetime.now() >= last_run + wait_time) or first_run:
            first_run = False
            last_run = datetime.now()
            last_run = round_time(last_run,timedelta(minutes=config1.wait_time), to='down')


            #run backtest with first config

            my_backtest1.initialise()
            my_backtest1.run()
            my_backtest1.report()

            image = my_backtest1.graph(save=config1.use_telegram)
            if config1.use_telegram:
                done=False
                fail_count=0
                while not done:
                    try:
                    # if True:
                        my_telegram.send_graph(image)
                        done=True
                        print('Sent to Telegram.')
                    # else:
                    except:
                        print('Sending failed.')
                        fail_count+=1
                        sleep(2^fail_count)
                        if fail_count > 9:
                            done=True

            # exit()
        sleep(1)


if __name__ == "__main__":
    main()
