from graphs.Graphs_class import *
import matplotlib.pyplot as plt

class Graph_Early_Onset_Trend(Graph):
    def __init__(self, **kwargs):
        super(Graph_Early_Onset_Trend, self).__init__(**kwargs)
        self.short_title = 'Early Onset Trend'

    def graph(self):
        # self.save=save
        self.strategy.bot.data_active = self.strategy.bot.data#.iloc[self.strategy.bot.get_warmup_candles():]
        fig, axs = plt.subplots(2, figsize=(15, 9.5))
        fig.suptitle(self.get_title())
        # line1 = axs[0].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['cci_mode_aj'],color='red', linewidth=0.75, zorder=4)
        # axs.set_ylim(0,40)

        # axs0=axs[0].twinx()

        # Draw candlesticks
        axs[0] = self.draw_all_candlesticks(axs[0])

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.strategy.bot.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs[0].plot(buy_x, buy_y, '^', color='blue', markersize=7, zorder=6)
        axs[0].plot(sell_x, sell_y, 'v', color='red', markersize=7, zorder=7)

        # line4 = axs[1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['0'],color='grey', linewidth=0.75)
        line4 = axs[1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['eoti_quotient1'],color='green', linewidth=0.75)
        line5 = axs[1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['eoti_quotient2'],color='red', linewidth=0.75)

        self.display()


    def graph_create(self):
        self.strategy.bot.data_active = self.strategy.bot.data #.iloc[self.get_warmup_candles():]
        self.fig, self.axs = plt.subplots(3, figsize=(15, 9.5))
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
        self.strategy.bot.data_active = self.strategy.bot.data #.iloc[self.get_warmup_candles():]
        # fig, axs = plt.subplots(3, figsize=(15, 9.5))
        fig.suptitle(self.strategy.bot.interval + ' CCI ' + self.strategy.bot.instrument.symbol + ' ' + str(self.strategy.bot.data_active['date_time'].tail(1).values[0][:19]))
        # Draw candlesticks
        line1 = axs[0].plot(self.strategy.bot.data['date_time'], self.strategy.bot.data['cci_mode_aj'],color='purple', linewidth=0.75)

        # axs0=axs[0].twinx()

        axs0 = draw_all_candlesticks(axs0, self.strategy.bot.data_active)
        # axs[0].set_yscale('log')
        line1 = axs0.plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['ss_mama'],color='pink', linewidth=0.75)
        line1 = axs0.plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['mama'],color='blue', linewidth=0.75, zorder=4)
        line1 = axs0.plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['fama'],color='purple', linewidth=0.75, zorder=5)

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.strategy.bot.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs0.plot(buy_x, buy_y, '^', color='blue', markersize=7, zorder=6)
        axs0.plot(sell_x, sell_y, 'v', color='red', markersize=7, zorder=7)

        # axs0b=axs[0].twinx()

        line4 = axs[1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['cci_real'],color='blue', linewidth=0.75)
        # axs1=axs[1].twinx()
        # line = axs1.plot(self.bot.data_active['date_time'], self.bot.data_active['detrender'],color='pink', linewidth=0.75)
        # line = axs1.plot(self.bot.data_active['date_time'], self.bot.data_active['ss_detrender'],color='purple', linewidth=0.75)

        line1 = axs[2].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['pc_fama'],color='black', linewidth=0.75, zorder=4)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.1]*len(self.bot.data),color='red', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [0.1]*len(self.bot.data),color='red', linewidth=0.75, zorder=1)
        # line1 = axs[2].plot(self.bot.data_active['date_time'], [-0.06]*len(self.bot.data),color='orange', linewidth=0.75, zorder=1)
        line1 = axs[2].plot(self.strategy.bot.data_active['date_time'], [0.00]*len(self.strategy.bot.data),color='grey', linewidth=0.75, zorder=1)
        # axs2 = axs[2].twinx()
        line = axs2.plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['cci_period_aj'],color='purple', linewidth=0.75)
        # axs2.set_ylim(0,100)

        plt.show(block=False)

