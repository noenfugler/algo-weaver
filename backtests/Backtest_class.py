#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from orders.Order_class import Order
from datasets.Datasets import *
from graphs.CCI_PC_fama_graph import *
from utils.util_functions import round_time

class Backtest():
    def __init__(self, **kwargs):
        print('Creating Backtest object')
        self.exchange = None
        self.instrument = kwargs['instrument']
        self.interval = kwargs['interval']
        # self.wait_time = kwargs['wait_time']
        self.exchange = kwargs['exchange']
        self.dataset = None
        self.data = None #current pd from dataset for row
        self.strategy = None
        self.indicators = None
        self.live = False
        self.starting_cash = None
        self.trading_cash = None
        self.starting_position = None
        self.ls_orders=[]
        self.ls_trades=[]
        self.ls_indicators = []
        self.trading_cash=0.0
        self.position = 0
        #exchange - exchange object
        #live - boolean to indicate whether backtesting or live trading
        #interval - candle interval

    def get_warmup_candles(self):
        highest_num=0
        for indicator in self.ls_indicators:
            if indicator.min_warmup_candles>highest_num:
                highest_num=indicator.min_warmup_candles
        return highest_num

    def run(self):
        print('Running Backtest')
        # self.initialise()
        self.execute()
        self.save_results()

    def create_indicators(self):
        for indicator in self.ls_indicators:
            indicator.create(self.dataset.data)

    def update_indicators(self):
        #end_datetime, start_datetime, num_candles.  Require 2 of the three or if only num_candles, assume end_datetime is last candle.
        #warmup_candles - candles to warm up indicators.  Not to be backtested.

        #initialise dataset
        #run indicators
        for indicator in self.ls_indicators:
            indicator.initialise(self.data)

    def get_last_datetime(self):
        last_row = len(self.data)-1
        return self.data.loc[last_row,'date_time']

    def get_last_close(self):
        return float(self.data.iloc[-1].loc['close'])

    def get_last_open(self):
        return float(self.data.iloc[-1].loc['open'])

    def modify_position(self, quantity):
        self.position += quantity
        
    def execute(self):
        if self.live:
            if self.dataset.new_data():
                self.data = self.dataset.get_next_candle()
                self.update_indicators()
                if self.strategy.should_long():
                    self.strategy.go_long()
                if self.strategy.should_short():
                    self.strategy.go_short()
        else:
            self.strategy.strategy_init()
            while not self.dataset.finished:
                print('.', end='')
                self.data = self.dataset.get_next_candle()
                self.strategy._candle_init()
                self.strategy.candle_init()

                # for indicator in self.ls_indicators:
                #     indicator.increment()
                #TODO: Restore above lines for live
                self.strategy.should_long_setup_trigger()
                if self.strategy.should_long():
                    this_order=self.strategy.go_long()
                    self.ls_orders.append(this_order)
                    self.ls_trades.append(this_order.fulfill(timestamp=this_order.timestamp, price=self.get_last_open()))  #TODO:  I think this timestamp is 1 too early.
                    # self.modify_position(this_order.quantity)
                self.strategy.should_short_setup_trigger()
                if self.strategy.should_short():
                    this_order=self.strategy.go_short()
                    self.ls_orders.append(this_order)
                    self.ls_trades.append(this_order.fulfill(timestamp=this_order.timestamp, price=self.get_last_open()))  #TODO:  I think this timestamp is 1 too early.
                    # self.modify_position(this_order.quantity)
                self.strategy.should_modify_long_setup_trigger()
                if self.strategy.should_modify_long():
                    this_order=self.strategy.modify_long()
                    self.ls_orders.append(this_order)
                    self.ls_trades.append(this_order.fulfill(timestamp=this_order.timestamp, price=self.get_last_open()))  #TODO:  I think this timestamp is 1 too early.
                    # self.modify_position(this_order.quantity)
                self.strategy.should_modify_short_setup_trigger()
                if self.strategy.should_modify_short():
                    this_order=self.strategy.modify_short()
                    self.ls_orders.append(this_order)
                    self.ls_trades.append(this_order.fulfill(bot=self, timestamp=this_order.timestamp, price=self.get_last_open()))  #TODO:  I think this timestamp is 1 too early.
                    # self.modify_position(this_order.quantity)
                self.strategy.candle_exit
            self.strategy.strategy_exit()


    def save_results(self):
        self.win_ratio = None
        self.profit_ratio = None
        pass

    def get_profit_ratio(self):
        pass

    def report(self):
        print("***********************")
        print("ORDERS")
        print("***********************")
        for order in self.ls_orders:
            print(order)

        print("***********************")
        print('TRADES')
        print("***********************")
        cash = self.starting_cash
        position = self.starting_position
        for trade in self.ls_trades:
            print(trade)
            if trade.side == "BUY":
                position += trade.quantity
                cash -= trade.price*trade.quantity  #negative due to quantity being + for buy and - for sell
            if trade.side == "SELL":
                position += trade.quantity
                cash -= trade.price*trade.quantity  #negative due to quantity being + for buy and - for sell
            print('cash', cash, 'position', position)

        #TODO: generate a full report on performance

    def graph(self, save):
        pass



