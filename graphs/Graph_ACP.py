#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from graphs.Graphs_class import *
import matplotlib.pyplot as plt
# import palettable.cartocolors.diverging as pcd
import palettable.cmocean.sequential as pcs
import colorcet as cc
import cmasher as cmr
import copy

class Graph_ACP(Graph):
    def __init__(self, **kwargs):
        super(Graph_ACP, self).__init__(**kwargs)
        self.short_title = 'ACP'
        self.acp_max=kwargs['acp_max']
        # self.cmap = cmr.neon                   # CMasher
        # self.cmap = cmr.pepper                   # CMasher
        self.cmap = cmr.rainforest                   # CMasher
        # self.cmap = plt.get_cmap('cmr.neon')   # MPL
        # self.cmap=cc.cm.kbc

    def graph(self, save=False):
        self.strategy.bot.data_active = copy.deepcopy(self.strategy.bot.data.iloc[self.strategy.bot.get_warmup_candles():,])
        fig, axs = plt.subplots(2,2, figsize=(15, 9.5))
        # axs=[]
        # axs[0,0]=axs2x2[0,0]
        # axs[1,0]=axs2x2[1,0]
        # axs[0,1]=axs2x2[0,1]
        # axs[1,1]=axs2x2[1,1]
        fig.suptitle(self.get_title())
        line1 = axs[0,0].plot(self.strategy.bot.data_active['date_time'], [0.5]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[0,0].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['acp2_strength'],color='purple', linewidth=0.75, zorder=4, alpha=1)
        line1 = axs[0,0].plot(self.strategy.bot.data_active['date_time'], -self.strategy.bot.data_active['acp3_strength'],color='pink', linewidth=0.75, zorder=4, alpha=1)
        axs[0,0].margins(0.0)
        axs0=axs[0,0].twinx()
        line1 = axs0.plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['mama'],color='blue', linewidth=0.75, zorder=4, alpha=1)

        # Draw candlesticks
        axs0 = self.draw_all_candlesticks(axs0)

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
        for i in range(10,200,10):
            ago10=self.strategy.bot.data_active.loc[len(self.strategy.bot.data)-i,'date_time']
            axs0.axvline(x=ago10, linewidth=0.5, color='black', alpha=0.5)

        index2 = []
        for i in range (8,self.acp_max+1):
            # index2.append('pwr_'+str(i))
            index2.append('acp2_'+str(i))
            # index2.append('sqsum_' + str(i))
        cols = [i for i in range(0,len(self.strategy.bot.data_active))]
        axs0.margins(0.0)
        axs[1,1].margins(0.0)
        axs[1,1].imshow(self.strategy.bot.data_active[index2].transpose().iloc[::-1], extent=[1, len(self.strategy.bot.data_active) ,8,self.acp_max+1], cmap=self.cmap)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [10]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [20]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [30]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [40]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [50]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [60]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [70]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [80]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], [90]*len(self.strategy.bot.data_active['acp2_strength']),color='black', linewidth=0.75, zorder=4, alpha=0.5)
        line1 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['acp2_period'], color='purple', linewidth=0.75, zorder=4, alpha=1)
        line2 = axs[1,1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['acp3_period'], color='pink', linewidth=0.75, zorder=4, alpha=1)

        line2 = axs[1,0].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['ccia_real'], color='blue', linewidth=0.75,
                            zorder=4, alpha=1)
        line2 = axs[1,0].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['ccia_imag'], color='red', linewidth=0.75,
                            zorder=4, alpha=1)
        axs[1,1].margins(0.0)
        # axs2=axs[0,1].twinx()
        axs[0,1].margins(0.0)

        line2 = axs[0,1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['acp_aj_period']/2, color='grey', linewidth=0.75, zorder=4, alpha=1)
        line2 = axs[0,1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['acp_aj_period'], color='black', linewidth=0.75, zorder=4, alpha=1)
        line2 = axs[0,1].plot(self.strategy.bot.data_active['date_time'], self.strategy.bot.data_active['ccia_cycle_count'], color='green', linewidth=0.75, zorder=4, alpha=1)

        index3 = []
        # df_graph = data.tail(include).head(include-drop_last_num_bars)
        for i in range (8,self.acp_max+1):
            # index3.append('pwr_'+str(i))
            index3.append('acp3_'+str(i))
            # index3.append('sqsum_' + str(i))This one2
        cols = [i for i in range(0,len(self.strategy.bot.data_active))]
        return self.display()

