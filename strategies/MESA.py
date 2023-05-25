#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from strategies.Strategy_class import Strategy
from crypto_trader_lib import HistoricalDataset
from indicators.MESA import indicator_MESA
import pandas as pd
import copy

class strategy_MESA(Strategy):
    def setup(self, source='binance', alpha=0.07):
        instrument=''
        self.usdt = 1000
        self.max_allocation = 0.1
        self.leverage = 20
        self.fee_percentage = 0.0004

        # self.source = 'excel'
        self.source = 'binance'
        # self.source='pickle'

        self.price_basis = 'oc'

        self.drop_last_num_bars = 0
        self.warmup_candles = 50

        # self.instrument = "BTCUSDT"
        self.instrument="ETHUSDT"

        # self.date_split = False
        self.silent = False
        self.trade_short = False
        self.load_data = False

        self.leverage=20

        self.stop_percent = 0.1

        self.candles = 100

        #TODO: Move most of the parameters below into the strategy rather than the dataset
        mydata = HistoricalDataset(interval='1h', source=self.source, instrument=self.instrument, trade_short=self.trade_short,
                                   leverage=self.leverage, price_basis=self.price_basis)
        pp_mydata = copy.deepcopy(mydata)
        pp_mydata.trade_short = True
        mydata.buy_earliest = 0
        mydata.buy_latest = 24
        mydata.snr_ratio_low = 1.0
        mydata.snr_ratio_high = 1.0

        pp_mydata.load_data(limit=self.candles + self.warmup_candles)
        pp_mydata.calc_derived_values()
        mydata.df = copy.deepcopy(pp_mydata.df)

        pp_mydata.strategy_pp_long_short(starting_balance_usdt=self.usdt, max_allocation=self.max_allocation, limit=self.candles + self.warmup_candles,
                                         fee_percentage=self.fee_percentage, leverage=mydata.leverage, source=source, reload_data=self.load_data, silent=self.silent)

        print('\n**********  MESA LONG SHORT  *************')

        mydata.load_data(limit = self.candles, source=source, date_split=False)
        mydata.calc_derived_values()
        my_MESA = indicator_MESA(mydata.df)
        my_MESA.create()

# df = pd.DataFrame([1,2,3])
my_strategy = strategy_MESA()
my_strategy.setup()
