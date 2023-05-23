#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

class Strategy():
    def __init__(self, kwargs):
        # if 'exchange' in kwargs:
        #     self.exchange = kwargs['exchange']
        # else:
        #     raise Exception('must pass in a exchange')

        if 'bot' in kwargs:
            self.bot = kwargs['bot']
        else:
            raise Exception('must pass in a bot')

        self.df = None
        self.btc=0.0
        self.usdt = None
        self.max_allocation = None
        self.leverage = None
        self.fee_percentage = None
        self.source = None
        self.instrument = None
        self.price_basis = None
        self.silent = None
        self.trade_short = None
        self.end_date = None
        self.stop_percent = None
        self.leverage = None
        self.candles = None
        self.load_data = None

        self.drop_last_num_bars = 0
        self.purchase_price = 0.0
        self.wins = 0
        self.losses = 0
        self.ls_win_percents = []
        self.ls_loss_percents = []
        self.ls_usdt = []
        self.stop_percent = None
        self.strategy_run = False
        self.data=None
        self.silent = kwargs['silent']  #TODO:  Should this be in the bot or the strategy?
        self.allow_long = kwargs['allow_long']
        self.allow_short = kwargs['allow_short']

        self.long_trigger = False
        self.modify_long_trigger = False
        self.short_trigger = False
        self.modify_short_trigger=False


    def _up(self, source):
        return self.bot.data.loc[self.last_row, source] > self.bot.data.loc[self.last_row - 1, source]

    def _down(self, source):
        return self.bot.data.loc[self.last_row, source] < self.bot.data.loc[self.last_row - 1, source]

    def _cross_over(self, source1, source2):
        return self.bot.data.loc[self.last_row-1, source1] > self.bot.data.loc[self.last_row-1, source2] and \
               self.bot.data.loc[self.last_row-2, source1] <= self.bot.data.loc[self.last_row-2, source2]

    def _cross_under(self, source1, source2):
        return self.bot.data.loc[self.last_row-1, source1] < self.bot.data.loc[self.last_row-1, source2] and \
               self.bot.data.loc[self.last_row-2, source1] >= self.bot.data.loc[self.last_row-2, source2]

    def _trough(self, source):
        return self.bot.data.loc[self.last_row-1, source] > self.bot.data.loc[self.last_row-2, source] and \
               self.bot.data.loc[self.last_row-3, source] >= self.bot.data.loc[self.last_row-2, source]

    def _peak(self, source):
        return self.bot.data.loc[self.last_row-1, source] < self.bot.data.loc[self.last_row-2, source] and \
               self.bot.data.loc[self.last_row-3, source] <= self.bot.data.loc[self.last_row-2, source]

    def strategy_init(self):
        pass

    def _candle_init(self):
        self.last_row = self.get_last_row_num()

    def candle_init(self):
        self.last_row = self.get_last_row_num()

    def should_long_setup_trigger(self):
        pass

    def should_long(self):
        pass

    def should_modify_long_setup_trigger(self):
        pass

    def should_modify_long(self):
        pass

    def should_short_setup_trigger(self):
        pass

    def should_short(self):
        pass

    def should_modify_short_setup_trigger(self):
        pass

    def should_modify_short(self):
        pass

    def go_long(self):
        pass

    def modify_long(self):
        pass

    def go_short(self):
        pass

    def modify_short(self):
        pass
    
    def candle_exit(self):
        pass

    def strategy_exit(self):
        pass

    def get_sharpe_ratio(self):
        pass

    def get_last_row_num(self):
        return len(self.bot.data)-1

