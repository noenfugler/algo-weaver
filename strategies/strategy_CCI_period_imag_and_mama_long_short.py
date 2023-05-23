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

class Strategy_CCI_period_imag_and_mama_long_short(Strategy):

    def should_long_setup_trigger(self):
        self.modify_long_trigger = self.bot.data.loc[last_row - 2, 'cci_imag'] < self.bot.data.loc[last_row - 1, 'cci_imag'] and \
                                    self.bot.data.loc[last_row - 2, 'cci_imag'] < self.bot.data.loc[last_row - 3, 'cci_imag']


    def should_long_trend(self):
        last_row = self.get_last_row_num()
        return self.bot.data.loc[last_row - 1, 'cci_mode_aj'] == 1

    def should_long_cycle(self):
        last_row = self.get_last_row_num()
        return self.bot.data.loc[last_row - 1, 'cci_mode_aj'] == 0 and \
               self.bot.data.loc[last_row - 2, 'cci_imag'] < self.bot.data.loc[last_row - 1, 'cci_imag'] and \
               self.bot.data.loc[last_row - 2, 'mama'] < self.bot.data.loc[last_row - 1, 'mama']

    def should_long(self):
        if self.bot.position > 0:
            return False
        else:
            return self.should_long_trend() or self.should_long_cycle()

    def should_modify_long_setup_trigger(self):
        self.modify_long_trigger = self.bot.data.loc[last_row - 2, 'cci_imag'] > self.bot.data.loc[last_row - 1, 'cci_imag'] and \
                                    self.bot.data.loc[last_row - 2, 'cci_imag'] > self.bot.data.loc[last_row - 3, 'cci_imag']

    def should_modify_long(self):
        if self.bot.position <= 0:
            return False
        else:
            return not (self.should_long_trend() or self.should_long_cycle())

    def should_short_trend(self):
        last_row = self.get_last_row_num()
        return self.bot.data.loc[last_row - 1, 'cci_mode_aj'] == -1

    def should_short_cycle(self):
        last_row = self.get_last_row_num()
        return self.bot.data.loc[last_row - 1, 'cci_mode_aj'] == 0 and \
               self.bot.data.loc[last_row - 2, 'cci_imag'] > self.bot.data.loc[last_row - 1, 'cci_imag'] and \
               self.bot.data.loc[last_row - 2, 'mama'] > self.bot.data.loc[last_row - 1, 'mama']

    def should_short(self):
        if self.bot.position < 0:
            return False
        else:
            return self.should_short_trend() or self.should_short_cycle()

    def should_modify_short(self):
        if self.bot.position >= 0:
            return False
        else:
            return not (self.should_short_trend() or self.should_short_cycle())

    def go_long(self):
        self.long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = self.bot.trading_cash / self.bot.get_last_close()
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
        self.short_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = -self.bot.trading_cash / self.bot.get_last_close()
        this_order.create_order(symbol=self.bot.instrument.symbol, side="SELL", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    def modify_short(self):
        self.modify_short_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = -self.bot.position
        this_order.create_order(symbol=self.bot.instrument.symbol, side="BUY", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    # def


