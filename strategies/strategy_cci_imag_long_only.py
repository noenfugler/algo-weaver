from strategies.Strategy_class import Strategy
from orders.Order_class import Order

class Strategy_CCI_imag_long_only(Strategy):

    def should_long(self):
        last_row = len(self.bot.data)
        if self.bot.position > 0:
            return False
        else:
            # if self.bot.data.loc[last_row - 1, 'cci_state'] == 1:
            #     return True
            # else:
            return self.bot.data.loc[last_row - 1, 'cci_imag'] > self.bot.data.loc[last_row-2, 'cci_imag'] and \
                   self.bot.data.loc[last_row - 1, 'cci_state'] == 0

    def should_modify_long(self):
        last_row = len(self.bot.data)
        if self.bot.position <= 0:
            return False
        else:
            # if self.bot.data.loc[last_row - 1, 'cci_state'] == -1:
            #     return True
            # else:
            return self.bot.data.loc[last_row-1, 'cci_imag'] < self.bot.data.loc[last_row-2, 'cci_imag'] and \
                   self.bot.data.loc[last_row - 1, 'cci_state'] == 0

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

