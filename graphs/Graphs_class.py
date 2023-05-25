#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
import matplotlib as mpl
import matplotlib.pyplot as plt


class Graph():
    def __init__(self, **kwargs):
        self.strategy=kwargs['strategy']
        self.save=kwargs['save']

    # Function to draw candlestick
    def draw_candlestick(self, axis, data, day, color_up, color_down):
        # Check if stock closed higher or not
        if data['close'] > data['open']:
            color = color_up
        else:
            color = color_down
        # Plot the candle wick
        axis.plot([day, day], [data['low'], data['high']], linewidth=0.5, color='black', solid_capstyle='round', zorder=2)
        # Draw the candle body
        rect = mpl.patches.Rectangle((day - 0.25, data['open']), 0.5, (data['close'] - data['open']), facecolor=color, edgecolor='black', linewidth=0.5, zorder=3)# Add candle body to the axis
        axis.add_patch(rect)
        # Return modified axis
        return axis


    # Function to draw all candlesticks
    def draw_all_candlesticks(self, axis, color_up='lightgreen', color_down='pink'):
        for day in range(self.strategy.bot.data_active.shape[0]):
            axis = self.draw_candlestick(axis, self.strategy.bot.data_active.iloc[day], day, color_up, color_down)
        return axis

    def draw_vline(self,axis,color='black', alpha=0.5, end_offset=10):
        end_day_num = self.strategy.bot.data_active.shape[0]
        axis = self.draw_candlestick(axis, self.strategy.bot.data_active.iloc[day], day, color_up, color_down)
        return axis

    def get_title(self):
        title = self.strategy.bot.interval + ' ' + self.short_title + ' ' + self.strategy.bot.instrument.symbol + ' ' + str(self.strategy.bot.data_active['date_time'].tail(1).values[0][:19])
        title=title.replace(":","-")
        return title

    def display(self):
        if self.save:
            file_path= '../chart_output/'+self.get_title()+'.png'
            plt.savefig(file_path)
            return file_path
        else:
            plt.show(block=True)

    def plot_variable_alpha(self,axis,x, y, alpha, color, linewidth, zorder):
        #Plots a line with variable alpha along the length
        for i in range(1,len(x)):
            axis.plot(x[i-1:i+1], y[i-1:i+1], alpha=abs(alpha[i:i+1].values[0]), color=color, linewidth=linewidth,zorder=zorder)
        return axis