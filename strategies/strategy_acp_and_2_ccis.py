#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from strategies.Strategy_class import Strategy
from orders.Order_class import Order
import matplotlib.pyplot as plt
from math import isinf


class Strategy_ACP_and_2_CCIs(Strategy):

    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Strategy_ACP_and_2_CCIs, self).__init__(kwargs)

    def should_long(self):
        last_row = self.get_last_row_num()
        if self.bot.position > 0:
            return False
        elif -(self.bot.data.loc[last_row,'acp3_strength']) * 1.2 > self.bot.data.loc[last_row,'acp2_strength'] and -(self.bot.data.loc[last_row,'acp3_strength']) > 0.5:
            return self.bot.data.loc[last_row, 'ccia_half_real'] > self.bot.data.loc[last_row, 'ccia_half_real']
        elif -(self.bot.data.loc[last_row,'acp3_strength']) * 1.2 < self.bot.data.loc[last_row,'acp2_strength'] and -(self.bot.data.loc[last_row,'acp2_strength']) > 0.5:
            return self.bot.data.loc[last_row, 'ccia_full_real'] > self.bot.data.loc[last_row, 'ccia_full_real']
        else:
            return False

    def should_modify_long(self):
        last_row = self.get_last_row_num()
        if self.bot.position <= 0:
            return False
        elif -(self.bot.data.loc[last_row,'acp3_strength']) * 1.2 > self.bot.data.loc[last_row,'acp2_strength'] and -(self.bot.data.loc[last_row,'acp3_strength']) > 0.5:
            return self.bot.data.loc[last_row, 'ccia_half_real'] < self.bot.data.loc[last_row, 'ccia_half_real']
        elif -(self.bot.data.loc[last_row,'acp3_strength']) * 1.2 < self.bot.data.loc[last_row,'acp2_strength'] and -(self.bot.data.loc[last_row,'acp2_strength']) > 0.5:
            return self.bot.data.loc[last_row, 'ccia_full_real'] < self.bot.data.loc[last_row, 'ccia_full_real']
        else:
            return False

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
        pass
