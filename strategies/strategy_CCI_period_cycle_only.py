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
from orders.Order_class import Order
import matplotlib.pyplot as plt
from utils.util_functions import *
from math import isinf


class Strategy_CCI_period_cycle_only(Strategy):

    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Strategy_CCI_period_cycle_only, self).__init__(kwargs)
            self.trend_factor=kwargs['trend_factor']

    def strategy_init(self):
        self.trough_zone = False
        self.peak_zone = False
        self.uptrend_failed=False

    def candle_init(self):
        self.last_row=self.get_last_row_num()
        if self._peak('cci_imag'):
            self.peak_zone = True
        if self._peak('cci_real'):
            self.peak_zone = False
        if self._trough('cci_imag'):
            self.trough_zone = True
        if self._trough('cci_real'):
            self.trough_zone = False

    def _should_long_trend(self):
        return False

    def _should_long_cycle(self):
        return not isinf(self.bot.data.loc[self.last_row, 'cci_period_aj']) and  self._cross_over('cci_imag', 'cci_real')

    def should_long(self):
        if self.bot.position > 0:
            return False
        else:
            return self._should_long_trend() or self._should_long_cycle()

    def _should_modify_long_trend(self):
        return False

    def _should_modify_long_cycle(self):
        return isinf(self.bot.data.loc[self.last_row, 'cci_period_aj']) or self._cross_under('cci_imag', 'cci_real')

    def should_modify_long(self):
        if self.bot.position <= 0:
            return False
        else:
            return self._should_modify_long_cycle() or self._should_modify_long_trend()

    def should_short(self):
        return False

    def should_modify_short(self):
        return False

    def go_long(self):
        self.long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = self.bot.trading_cash / self.bot.get_last_close()  #TODO: Confirm if correct??
        this_order.create_order(symbol=self.bot.instrument.symbol, side="BUY", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    def modify_long(self):
        self.modify_long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = -self.bot.position
        this_order.create_order(symbol=self.bot.instrument.symbol, side="SELL", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    def go_short(self):
        return None

    def modify_short(self):
        return None

    def graph(self):
        self.bot.data_active = self.bot.data #.iloc[self.get_warmup_candles():]
        fig, axs = plt.subplots(2, figsize=(15, 9.5))
        fig.suptitle(self.bot.interval + ' CCI ' + self.bot.instrument.symbol + ' ' + str(self.bot.data_active['date_time'].tail(1).values[0][:19]))
        # Draw candlesticks
        line1 = axs[0].plot(self.bot.data['date_time'], self.bot.data['cci_mode_aj'],color='purple', linewidth=0.75)

        axs0=axs[0].twinx()

        axs0 = draw_all_candlesticks(axs0, self.bot.data_active)
        # axs[0].set_yscale('log')
        line1 = axs0.plot(self.bot.data_active['date_time'], self.bot.data_active['ss_mama'],color='pink', linewidth=0.75)
        line1 = axs0.plot(self.bot.data_active['date_time'], self.bot.data_active['mama'],color='blue', linewidth=0.75, zorder=4)
        line1 = axs0.plot(self.bot.data_active['date_time'], self.bot.data_active['fama'],color='purple', linewidth=0.75, zorder=5)

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.bot.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs0.plot(buy_x, buy_y, '^', color='blue', markersize=7, zorder=6)
        axs0.plot(sell_x, sell_y, 'v', color='red', markersize=7, zorder=7)

        line4 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_real'],color='blue', linewidth=0.75)
        line = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['bs_wave'],color='pink', linewidth=0.75)

        axs1=axs[1].twinx()
        axs1.set_ylim(0,50)
        line = axs1.plot(self.bot.data_active['date_time'], self.bot.data_active['cci_period_aj'],color='purple', linewidth=0.75)


        plt.show()
