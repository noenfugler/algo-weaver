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

class Strategy_CCI_re_im_cross_long_only(Strategy):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Strategy_CCI_re_im_cross_long_only, self).__init__(kwargs)

    def candle_init(self):
        pass


    def should_long(self):
        last_row = len(self.bot.data)
        if self.bot.position > 0:
            return False
        else:
            # if self.bot.data.loc[last_row - 1, 'cci_state'] == 1:
            #     return True
            # else:
            return self.bot.data.loc[last_row - 1, 'cci_imag'] > self.bot.data.loc[last_row - 1, 'cci_real'] and \
                   self.bot.data.loc[last_row - 2, 'cci_imag'] < self.bot.data.loc[last_row - 2, 'cci_real'] and \
                   self.bot.data.loc[last_row - 1, 'cci_mode_aj'] == 0

    def should_modify_long(self):
        last_row = len(self.bot.data)
        if self.bot.position <= 0:
            return False
        else:
            # if self.bot.data.loc[last_row - 1, 'cci_state'] == -1:
            #     return True
            # else:
            return self.bot.data.loc[last_row - 1, 'cci_imag'] < self.bot.data.loc[last_row - 1, 'cci_real'] and \
                   self.bot.data.loc[last_row - 2, 'cci_imag'] > self.bot.data.loc[last_row - 2, 'cci_real'] and \
                   self.bot.data.loc[last_row - 1, 'cci_mode_aj'] == 0

    def should_short(self):
        return False

    def should_modify_short(self):
        return False

    def go_long(self):
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = self.bot.trading_cash / self.bot.get_last_close()
        this_order.create_order(symbol=self.bot.instrument.symbol, side="BUY", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime(), )
        return this_order

    def modify_long(self):
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

    # def

    def graph(self):
        self.bot.data_active = self.bot.data #.iloc[self.get_warmup_candles():]
        fig, axs = plt.subplots(3, figsize=(15, 9.5))
        fig.suptitle(self.bot.interval + ' CCI ' + self.bot.instrument.symbol + ' ' + str(self.bot.data_active['date_time'].tail(1).values[0][:19]))
        axs[0].set_yscale('log')
        # axs[0].set_ylim(50000,80000)
        line1 = axs[0].plot(self.bot.data_active['date_time'], self.bot.data_active['close'],color='black', linewidth=0.75)
        line1 = axs[0].plot(self.bot.data_active['date_time'], self.bot.data_active['ss_mama'],color='green', linewidth=0.75)

        axs2=axs[0].twinx()
        line1 = axs2.plot(self.bot.data['date_time'], self.bot.data['cci_mode_aj'],color='purple', linewidth=0.75)
        line4 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_real'],color='blue', linewidth=0.75)
        axs[2].set_ylim(0,50)
        line = axs[2].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_period_aj'],color='red', linewidth=0.75)

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

        axs[0].plot(buy_x, buy_y, '^', color='blue', markersize=7)
        axs[0].plot(sell_x, sell_y, 'v', color='red', markersize=7)

        plt.show()

