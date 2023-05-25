#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

#Ehlers Autocorrelation Filter indicator

from indicators.Indicator_class import Indicator

import math

class Indicator_ACP_filt(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, source='close', lp_length=10, hp_length=48):
        data['HP'] = 0.0
        data['filt'] = 0.0
        data['filt_period'] = 0
        data['filt_period_plus'] = 0
        data['filt_period_indicator'] = 0
        data['filt_trend_mode'] = 0
        last_peak_row = 0
        last_trough_row=0
        # last_period = 0
        alpha1 = (math.cos(.707*2*math.pi / hp_length) + math.sin(.707*2*math.pi / hp_length) - 1) / math.cos(.707*2*math.pi / hp_length)

        a1 = math.exp(-1.414 * 2 * math.pi / lp_length)
        b1 = 2 * a1 * math.cos(1.414 * math.pi / lp_length)
        c2 = b1
        c3 = -a1 ** 2
        c1 = 1 - c2 - c3

        for row_num in range(2,len(data)):
            data.at[row_num, 'HP'] = (1 - alpha1 / 2) * (1 - alpha1 / 2) * (data.loc[row_num, source] - 2 * data.loc[row_num-1, source] + \
                        data.loc[row_num-2, source]) + 2 * (1 - alpha1) * data.loc[row_num-1, 'HP'] - (1 - alpha1) * (1 - alpha1) * \
                        data.loc[row_num-2, 'HP']
            #smooth with a super smoother filter
            data.at[row_num, 'filt'] = c1 * (data.loc[row_num, 'HP'] + data.loc[row_num-1, 'HP']) / 2 + c2 * data.loc[row_num-1, 'filt'] + c3 * data.loc[row_num-2, 'filt']
            if data.loc[row_num-2, 'filt'] > data.loc[row_num-1, 'filt'] and \
                    data.loc[row_num, 'filt'] > data.loc[row_num-1, 'filt']:
                last_trough_row = row_num-1
                data.loc[row_num,'filt_period'] = last_trough_row - last_peak_row
                data.loc[row_num,'filt_period_indicator'] = 0 #-last_period
                # last_period = last_trough_row - last_peak_row
            elif data.loc[row_num-2, 'filt'] < data.loc[row_num-1, 'filt'] and \
                    data.loc[row_num, 'filt'] < data.loc[row_num-1, 'filt']:
                last_peak_row = row_num-1
                data.loc[row_num,'filt_period'] = last_peak_row - last_trough_row
                data.loc[row_num,'filt_period_indicator'] = 0 #-last_period
                # last_period = last_peak_row - last_trough_row
            else:
                data.at[row_num,'filt_period'] = data.loc[row_num-1,'filt_period']
                data.at[row_num, 'filt_period_indicator'] = data.loc[row_num-1,'filt_period_indicator'] + 1
            data.at[row_num,'filt_period_plus'] = data.loc[row_num,'filt_period']+1
            if data.loc[row_num,'filt_period_indicator'] > data.loc[row_num,'filt_period_plus']:
                if data.loc[row_num, 'filt'] > data.loc[row_num-1, 'filt']:
                    data.at[row_num,'filt_trend_mode']=1
                else:
                    data.at[row_num, 'filt_trend_mode'] = -1
            else:
                data.at[row_num, 'filt_trend_mode'] = 0
            # data.at[row_num, 'filt_period_ss'] = c1 * (data.loc[row_num, 'filt_period'] + data.loc[row_num-1, 'filt_period']) / 2 + c2 * data.loc[row_num-1, 'filt_period_ss'] + c3 * data.loc[row_num-2, 'filt_period_ss']
            # data.at[row_num, 'filt_period_ss'] = 0.7 * data.loc[row_num, 'filt_period'] + 0.3*data.loc[row_num-1, 'filt_period_ss']

        # data['filt_momentum']=data['filt']*2 - data['filt'].shift(1)
        # data['filt_momentum']=data['filt_momentum'].fillna(0)

        # data['filt_momentum_ss'] = 0.0
        # for row_num in range(2,len(data)):
        #     data.at[row_num, 'filt_momentum_ss'] = c1 * (data.loc[row_num, 'filt_momentum'] + data.loc[row_num - 1, 'filt_momentum']) / 2 + c2 * data.loc[row_num - 1, 'filt_momentum_ss'] + c3 * data.loc[row_num - 2, 'filt_momentum_ss']
