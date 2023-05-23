from strategies.Strategy_class import Strategy
from orders.Order_class import Order
import matplotlib.pyplot as plt
from utils.util_functions import *
from math import isinf


class Strategy_pc_fama_cross_zero(Strategy):

    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Strategy_pc_fama_cross_zero, self).__init__(kwargs)
            # self.trend_factor=kwargs['trend_factor']

    def strategy_init(self):
        pass

    def candle_init(self):
        self.last_row=self.get_last_row_num()

    def should_long(self):
        return self.bot.position <= 0 and self.bot.data.loc[self.last_row, 'pc_fama']>0.2

    def should_modify_long(self):
        return self.bot.position > 0 and self.bot.data.loc[self.last_row, 'pc_fama']<=0

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
        fig, axs = plt.subplots(3, figsize=(15, 9.5))
        fig.suptitle(self.bot.interval + ' CCI ' + self.bot.instrument.symbol + ' ' + str(self.bot.data_active['date_time'].tail(1).values[0][:19]))
        # Draw candlesticks
        # line1 = axs[0].plot(self.bot.data['date_time'], self.bot.data['cci_mode_aj'],color='purple', linewidth=0.75)

        axs0=axs[0].twinx()

        axs0 = draw_all_candlesticks(axs0, self.bot.data_active)
        # axs[0].set_yscale('log')
        # line = axs0.plot(self.bot.data_active['date_time'], self.bot.data_active['aj_avg_long'],color='black', linewidth=0.75)

        # line1 = axs0.plot(self.bot.data_active['date_time'], self.bot.data_active['ss_mama'],color='pink', linewidth=0.75)
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

        axs0b=axs[0].twinx()

        line4 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_real'],color='blue', linewidth=0.75)
        axs1=axs[1].twinx()
        line = axs1.plot(self.bot.data_active['date_time'], self.bot.data_active['cci_period_aj'],color='purple', linewidth=0.75)

        line1 = axs[2].plot(self.bot.data_active['date_time'], self.bot.data_active['pc_fama'],color='black', linewidth=0.75, zorder=4)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.25]*len(self.bot.data),color='red', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [0.25]*len(self.bot.data),color='red', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.1]*len(self.bot.data),color='orange', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [0.1]*len(self.bot.data),color='orange', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.06]*len(self.bot.data),color='yellow', linewidth=0.75, zorder=1)
        line1 = axs[2].plot(self.bot.data_active['date_time'], [0.0]*len(self.bot.data),color='grey', linewidth=0.5, zorder=1)
        # axs[2].set_ylim(-0.4,0.4)
        # axs2 = axs[2].twinx()
        # axs2.set_ylim(0,100)
        # line = axs2.plot(self.bot.data_active['date_time'], self.bot.data_active['detrender'],color='pink', linewidth=0.75)
        # line = axs2.plot(self.bot.data_active['date_time'], self.bot.data_active['ss_detrender'],color='purple', linewidth=0.75)
        # line1 = axs[3].plot(self.bot.data_active['date_time'], [0]*len(self.bot.data),color='grey', linewidth=0.5)
        # line1 = axs[3].plot(self.bot.data_active['date_time'], self.bot.data_active['trend_aj'],color='purple', linewidth=0.75)
        # line1 = axs[3].plot(self.bot.data_active['date_time'], self.bot.data_active['ss_trend_aj'],color='black', linewidth=0.75)

        plt.show()

    def graph_create(self):
        self.bot.data_active = self.bot.data #.iloc[self.get_warmup_candles():]
        self.fig, self.axs = plt.subplots(3, figsize=(15, 9.5))
        # self.fig.suptitle(self.bot.interval + ' CCI ' + self.bot.instrument.symbol + ' ' + str(self.bot.data_active['date_time'].tail(1).values[0][:19]))
        self.axs0=axs[0].twinx()
        self.axs0b=axs[0].twinx()
        self.axs1=axs[1].twinx()
        self.axs2 = axs[2].twinx()
        self.axs2.set_ylim(0,100)
        plt.show(block=False)

    def graph_clear(self):
        for artist in self.fig.gca().lines + self.fig.gca().collections:
            artist.remove()

    def graph_populate(self):
        self.bot.data_active = self.bot.data #.iloc[self.get_warmup_candles():]
        # fig, axs = plt.subplots(3, figsize=(15, 9.5))
        fig.suptitle(self.bot.interval + ' CCI ' + self.bot.instrument.symbol + ' ' + str(self.bot.data_active['date_time'].tail(1).values[0][:19]))
        # Draw candlesticks
        line1 = axs[0].plot(self.bot.data['date_time'], self.bot.data['cci_mode_aj'],color='purple', linewidth=0.75)

        # axs0=axs[0].twinx()

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

        # axs0b=axs[0].twinx()

        line4 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_real'],color='blue', linewidth=0.75)
        # axs1=axs[1].twinx()
        # line = axs1.plot(self.bot.data_active['date_time'], self.bot.data_active['detrender'],color='pink', linewidth=0.75)
        # line = axs1.plot(self.bot.data_active['date_time'], self.bot.data_active['ss_detrender'],color='purple', linewidth=0.75)

        line1 = axs[2].plot(self.bot.data_active['date_time'], self.bot.data_active['pc_fama'],color='black', linewidth=0.75, zorder=4)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.1]*len(self.bot.data),color='red', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [0.1]*len(self.bot.data),color='red', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.06]*len(self.bot.data),color='orange', linewidth=0.75, zorder=1)
        line1 = axs[2].plot(self.bot.data_active['date_time'], [0.00]*len(self.bot.data),color='grey', linewidth=0.75, zorder=1)
        # axs2 = axs[2].twinx()
        line = axs2.plot(self.bot.data_active['date_time'], self.bot.data_active['cci_period_aj'],color='purple', linewidth=0.75)
        # axs2.set_ylim(0,100)

        plt.show(block=False)

