from backtests.Backtest_class import Backtest
from strategies.acp_filt import Strategy_ACP_filt
from instruments.Instrument_BTCUSDT import Instrument_BTCUSDT
from exchanges.Exchange_Binance import Exchange_Binance_Futures
from datasets.Binance_Futures_BTCUSDT_1h_250_candles import Dataset_Binance_Futures_BTCUSDT_1h_250_candles
from indicators.ACP_filt import Indicator_ACP_filt

class Backtest_CCI_BTC_1h(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_CCI_BTC_1h, self).__init__(kwargs)
        else:
            super(Backtest_CCI_BTC_1h, self).__init__()

    def initialise(self, **kwargs):

        self.trading_cash=1000.0

        self.exchange = Exchange_Binance_Futures(self)
        self.exchange.initialise()

        acp_filt = Indicator_ACP_filt()
        self.ls_indicators.append(acp_filt)

        self.strategy = Strategy_ACP_filt(silent=False, trade_short=False, bot=self)

        self.instrument = Instrument_BTCUSDT()

        self.interval = '1h'

        self.live=False

        self.dataset = Dataset_Binance_Futures_BTCUSDT_1h_250_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      num_candles=250, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)
        self.dataset.load_data()
        self.create_indicators()



my_backtest = Backtest_CCI_BTC_1h()
my_backtest.initialise()
my_backtest.run()
    my_backtest.report()