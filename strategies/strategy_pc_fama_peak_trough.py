from strategies.Strategy_class import Strategy
from orders.Order_class import Order
import matplotlib.pyplot as plt
from utils.util_functions import *
from math import isinf


class Strategy_pc_fama_peak_trough(Strategy):

    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Strategy_pc_fama_peak_trough, self).__init__(kwargs)
            # self.trend_factor=kwargs['trend_factor']

    def strategy_init(self):
        pass

    def candle_init(self):
        self.last_row=self.get_last_row_num()

    def should_long(self):
        if self.allow_long:
            return self.bot.position <= 0 and self._trough('pc_fama')
        else:
            return False

    def should_modify_long(self):
        if self.allow_long:
            return self.bot.position > 0 and self._peak('pc_fama')
        else:
            return False

    def should_short(self):
        if self.allow_short:
            return self.should_modify_long()
        else:
            return False

    def should_modify_short(self):
        if self.allow_short:
            return self.should_long()
        else:
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
        self.long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = -self.bot.trading_cash / self.bot.get_last_close()  #TODO: Confirm if correct??
        this_order.create_order(symbol=self.bot.instrument.symbol, side="SELL", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    def modify_short(self):
        self.modify_long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = self.bot.position
        this_order.create_order(symbol=self.bot.instrument.symbol, side="BUY", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

