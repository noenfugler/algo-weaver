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
# from crypto_trader_lib import HistoricalDataset
from indicators.ACP_filt import indicator_ACP_filt
import matplotlib.pyplot as plt

import copy

class strategy_ACP_filt(Strategy):
    def setup(self, exchange):
        instrument=''
        self.starting_bal = 1000.0
        self.usdt = self.starting_bal
        self.btc = 0.0
        self.max_allocation = 0.4
        self.leverage = 20
        self.fee_percentage = 0.0004  #TODO: Create an exchange class and move this there.

        # self.source = 'excel'
        self.source = 'binance'
        # self.source='pickle'

        self.price_basis = 'c'

        self.drop_last_num_bars = 0
        self.warmup_candles = 50

        # self.instrument = "BTCUSDT"
        # self.instrument = "LTCUSDT"
        # self.instrument = "BCHUSDT"
        self.instrument="ETHUSDT"

        # self.interval = '15m'
        self.interval = '1h'

        # self.date_split = False
        self.silent = False
        self.trade_short = False
        self.load_data = False  #TODO: could be removed
        self.date_split = False

        self.leverage= 20
        self.stop_percent = 0.1
        self.candles = 250

        self.num_points = self.candles
        self.drop_last_num_bars = 0

        #TODO: Move most of the parameters below into the strategy rather than the dataset
        self.pp_mydata = HistoricalDataset(interval=self.interval, source=self.source, instrument=self.instrument, trade_short=self.trade_short,
                                   leverage=self.leverage, price_basis=self.price_basis)
        # self.pp_mydata = copy.deepcopy(self.mydata)
        self.pp_mydata.trade_short = True
        self.pp_mydata.buy_earliest = 0
        self.pp_mydata.buy_latest = 24
        self.pp_mydata.snr_ratio_low = 1.0
        self.pp_mydata.snr_ratio_high = 1.0

        self.pp_mydata.load_data(limit=self.candles + self.warmup_candles, date_split=self.date_split)
        self.pp_mydata.calc_derived_values()
        self.pp_mydata.max_allocation=self.max_allocation  #TODO: Move to parent class
        self.pp_mydata.fee_percentage = self.fee_percentage  #TODO: Move to parent class

        self.mydata = copy.deepcopy(self.pp_mydata)

        self.pp_mydata.strategy_pp_long_short(starting_balance_usdt=self.usdt, max_allocation=self.max_allocation, limit=self.candles + self.warmup_candles,
                                         fee_percentage=self.fee_percentage, leverage=self.mydata.leverage, source=source, reload_data=self.load_data, silent=True)

        print('\n**********  ACP FILT LONG SHORT  *************')
        # self.mydata.max_allocation=self.max_allocation  #TODO: Move to parent class
        # self.mydata.fee_percentage = self.fee_percentage  #TODO: Move to parent class

        # self.mydata.load_data(limit = self.candles, source=source, date_split=False)
        # self.mydata.calc_derived_values()
        # self.mydata
        my_filt = indicator_ACP_filt(self.mydata.df)
        my_filt.create()

    def execute(self):
        self.mydata.btc = self.btc
        self.mydata.usdt = self.usdt
        self.mydata.ls_usdt = []
        self.mydata.wins=0
        self.mydata.losses=0
        self.mydata.ls_win_percents=[]
        self.mydata.ls_loss_percents=[]
        for row_num in range(self.warmup_candles, len(self.mydata.df)):
            if self.mydata.df.loc[row_num-1, 'filt'] >  self.mydata.df.loc[row_num-2, 'filt'] and \
                    self.mydata.df.loc[row_num - 3, 'filt'] >  self.mydata.df.loc[row_num-2, 'filt']:
                message='Trough.  Go Long.'
                self.mydata.strategy_go_long(row_num, message=message)
            elif self.mydata.df.loc[row_num-1, 'filt'] < self.mydata.df.loc[row_num-2, 'filt'] and \
                    self.mydata.df.loc[row_num - 3, 'filt'] < self.mydata.df.loc[row_num - 2, 'filt']:
                if self.trade_short:        #go short
                    message='Peak.  Go Short.'
                    self.mydata.strategy_go_short(row_num, message=message)
                else:
                    message = 'Peak.  Exit position'
                    self.mydata.strategy_sell(row_num, message=message)

            # if stop gets triggered then sell
            if self.mydata.btc < 0.0: #short
                if self.mydata.df.loc[row_num-1,'high']/self.purchase_price > (1+self.stop_percent):
                    self.mydata.strategy_sell(row_num, (self.purchase_price*(1+self.stop_percent)))
                    print(self.mydata.df.loc[row_num,'date_time'], "Stop Sell", self.df.loc[row_num,'high'])

            elif self.mydata.btc > 0.0: #long
                if self.mydata.df.loc[row_num-1,'low']/self.purchase_price < (1-self.stop_percent):
                    self.mydata.strategy_sell(row_num, (self.purchase_price*(1-self.stop_percent)))
                    print(self.mydata.df.loc[row_num,'date_time'], "Stop Sell", self.df.loc[row_num,'low'])

            if row_num == len(self.mydata.df) - 1 and self.mydata.btc == 0.0:
                print("OUT OF MARKET AT LAST ROW")

            #TODO: Move to parent class
            # if last row then sell
            if row_num == len(self.mydata.df)-1 and self.mydata.btc != 0.0:
                if self.mydata.btc > 0 :
                    print("LONG AT LAST ROW")
                elif self.mydata.btc < 0:
                    print("SHORT AT LAST ROW")
                self.mydata.strategy_sell(row_num)
                print(self.mydata.df.loc[row_num,'date_time'], "End Sell", self.mydata.df.loc[row_num,'open'])

            # if last row then REPORT LAST TWO ROWS
            if row_num == len(self.mydata.df)-1:
                print("Last Bar", self.mydata.df.loc[row_num,'date_time'])
                print("USDT", self.mydata.df.loc[row_num,'usdt'])
            if self.mydata.df.loc[row_num,'position']==-2:
                self.mydata.df.at[row_num,'position']=self.mydata.df.loc[row_num-1,'position']

            self.mydata.df.at[row_num, 'btc'] = self.mydata.btc
            self.mydata.df.at[row_num, 'usdt'] = self.mydata.usdt

    def show_graph(self):
        fig, axs = plt.subplots(3, figsize=(16, 9.5))
        fig.suptitle(self.interval + ' ACP filter Indicator ' + self.instrument + ' - '+ str(self.mydata.df['date_time'].tail(1).values[0][:19]))
        date_times = self.mydata.df['short_date_time'].tail(self.num_points)
        line1 = axs[0].plot(date_times.head(self.num_points-self.drop_last_num_bars), self.mydata.df['filt_trend_mode'].tail(self.num_points).head(self.num_points-self.drop_last_num_bars), color='green',linewidth = 0.75)
        axs0 = axs[0].twinx()
        axs0.set_yscale('log')
        line2 = axs0.plot(date_times.head(self.num_points-self.drop_last_num_bars), self.mydata.df['close'].tail(self.num_points).head(self.num_points-self.drop_last_num_bars), color='black',linewidth = 0.75)
        line3 = axs[1].plot(date_times.head(self.num_points-self.drop_last_num_bars), self.mydata.df['filt'].tail(self.num_points).head(self.num_points-self.drop_last_num_bars), color='black',linewidth = 0.75)
        line4 = axs[2].plot(date_times.head(self.num_points-self.drop_last_num_bars), self.mydata.df['filt_period'].tail(self.num_points).head(self.num_points-self.drop_last_num_bars), color='red',linewidth = 0.75)
        line5 = axs[2].plot(date_times.head(self.num_points-self.drop_last_num_bars), self.mydata.df['filt_period_plus'].tail(self.num_points).head(self.num_points-self.drop_last_num_bars), color='black',linewidth = 0.75)
        line5 = axs[2].plot(date_times.head(self.num_points-self.drop_last_num_bars), self.mydata.df['filt_period_indicator'].tail(self.num_points).head(self.num_points-self.drop_last_num_bars), color='blue',linewidth = 0.75)
        plt.show()

my_strategy = strategy_ACP_filt()
my_strategy.setup()
my_strategy.execute()
my_strategy.mydata.strategy_report(starting_bal=my_strategy.starting_bal)
my_strategy.show_graph()
