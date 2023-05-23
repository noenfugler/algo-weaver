#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, exp
# from math import isinf
from pandas import NA, isna

class Indicator_ACP(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', avg_length=3, lp_length=10, hp_length=48, acp_max=48, alpha2=0.7, hp_filt=False, lp_filt=False):

        # hp_length=15
        alpha1 = (cos(.707 * 2 * pi / hp_length) + sin(.707 * 2 * pi / hp_length) - 1) / cos(.707 * 2 * pi / hp_length)
        data['HP'] = data[source]
        data['filt'] = 0.0
        data['acp_period'] = 0
        data['acp_period_smooth'] = 0
        data['acp_dominant_cycle'] = 0
        data['acp_last_peak'] = 0
        data['acp_last_trough'] = 0
        data['acp_aj_period'] = 0

        a1 = exp(-1.414 * 2 * pi / lp_length)
        b1 = 2 * a1 * cos(1.414 * pi / lp_length)
        c2 = b1
        c3 = -a1 ** 2
        c1 = 1 - c2 - c3
        if hp_filt:
            for row_num in range(max(2, avg_length), len(data)):
                data.at[row_num, 'HP'] = (1 - alpha1 / 2) * (1 - alpha1 / 2) * (
                            data.loc[row_num, source] - 2 * data.loc[row_num - 1, source] + \
                            data.loc[row_num - 2, source]) + 2 * (1 - alpha1) * data.loc[row_num - 1, 'HP'] - (1 - alpha1) * (1 - alpha1) * \
                            data.loc[row_num - 2, 'HP']


        if lp_filt:
            # smooth with a super smoother filter
            for row_num in range(max(2, avg_length), len(data)):
                data.at[row_num, 'filt'] = c1 * (data.loc[row_num, 'HP'] + data.loc[row_num - 1, 'HP']) / 2 + c2 * data.loc[
                row_num - 1, 'filt'] + c3 * data.loc[row_num - 2, 'filt']
        else:
            data['filt'] = data['HP']

        for lag in range(0, acp_max + 1):
            data['acp_' + str(lag)] = 0.0
            if avg_length == 0:
                M = lag
            else:
                M = avg_length
            # X=data['filt'].rolling(window=M)
            # Y=data['filt'].shift(lag).rolling(window=M)
            # corr, _ = pearsonr(X,Y)
            data['acp_' + str(lag)] = data['filt'].rolling(window=M).corr(data['filt'].shift(lag).rolling(window=M))
            # data['acp_' + str(lag)] = (1.0 + data['acp_' + str(lag)]) / 2
            data['acp_' + str(lag)] = data['acp_' + str(lag)].fillna(0)
            data['R1_' + str(lag)] = NA
            data['R2_' + str(lag)] = NA
        # print()
        # calc acp period
        last_period_row = max(3, avg_length) - 2  # TODO: NOT SURE WHAT THIS DOES
        for row_num in range(max(2, avg_length), len(data)):  # TODO: NOT SURE WHY THIS MIN
            for period in range(2, acp_max + 1):
                data.at[row_num, 'acp_cosinepart_' + str(period)] = 0.0
                data.at[row_num, 'acp_sinepart_' + str(period)] = 0.0
                for N in range(3, acp_max + 1):
                    # sr = cos(2*pi*period*N/(acp_max+1))
                    # si = -sin(2*pi*period*N/(acp_max+1))
                    data.at[row_num, 'acp_cosinepart_' + str(period)] = data.loc[row_num, 'acp_cosinepart_' + str(period)] + data.loc[
                        row_num, 'acp_' + str(period)] * cos((370 / 360 * 2 * pi * N / period))
                    # data.at[row_num, 'acp_cosinepart_' + str(period)] = data.loc[row_num,'acp_cosinepart_'+str(period)] + data.loc[row_num,'filt']*cos((2*pi * N * period/(acp_max+1)))
                    data.at[row_num, 'acp_sinepart_' + str(period)] = data.loc[row_num, 'acp_sinepart_' + str(period)] + data.loc[
                        row_num, 'acp_' + str(period)] * sin((370 / 360 * 2 * pi * N / period))
                    # data.at[row_num, 'acp_sinepart_' + str(period)] = data.loc[row_num,'acp_sinepart_'+str(period)] + data.loc[row_num,'filt']*sin((2*pi * N * period/(acp_max+1)))
                data.at[row_num, 'sqsum_' + str(period)] = data.loc[row_num, 'acp_cosinepart_' + str(period)] ** 2 + data.loc[
                    row_num, 'acp_sinepart_' + str(period)] ** 2
            # for period in range(10,49):
            # for period in range(8, acp_max + 1):
                # if not isna(data.at[row_num-1, 'R1_' + str(period)]):
                #     data.at[row_num, 'R2_' + str(period)] = data.loc[row_num-1, 'R1_' + str(period)]
                # else:
                #     data.at[row_num, 'R2_' + str(period)] = 0.0
                # data.at[row_num, 'R1_' + str(period)] = 0.2 * data.loc[row_num, 'sqsum_' + str(period)] ** 2 + 0.8 * data.loc[
                #     row_num, 'R2_' + str(period)]
                data.at[row_num, 'R1_' + str(period)] = data.loc[row_num, 'sqsum_' + str(period)]

            # find maximum power level for normalisation
            maxpwr = 0.0

            # for period in range(8, acp_max + 1):
            #     if data.loc[row_num, 'R1_' + str(period)] > maxpwr:
            #         maxpwr = data.loc[row_num, 'R1_' + str(period)]
            #         data.at[row_num, 'acp_maxpower'] = period
            for period in range(8, acp_max + 1):
                data.at[row_num, 'pwr_' + str(period)] = data.loc[row_num, 'R1_' + str(period)] #/ maxpwr

            # Compute the dominant cycle using the CG of the spectrum
            # From internet
            # peak_power = 0.0
            # for period in range(8,acp_max+1):
            #     if data.at[row_num,'pwr_'+str(period)] > peak_power:
            #         peak_power = data.at[row_num,'pwr_'+str(period)]
            #
            # spx=0
            # sp=0
            # for period in range(8,acp_max+1):
            #     if peak_power >=0.25 and data.loc[row_num,'pwr_'+str(period)] > 0.25:
            #         spx=spx + period * data.loc[row_num,'pwr_'+str(period)]
            #         sp=sp + data.loc[row_num,'pwr_'+str(period)]
            # if sp != 0 :
            #     data.at[row_num,'acp_dominant_cycle']=spx/sp
            # if sp<0.25 :
            #     data.at[row_num, 'acp_dominant_cycle'] = data.at[row_num-1, 'acp_dominant_cycle']

            # Original Ehlers
            spx = 0.0
            sp = 0.0
            for period in range(8, acp_max + 1):
                if data.loc[row_num, 'pwr_' + str(period)] > 0.5:
                    spx = spx + period * data.loc[row_num, 'pwr_' + str(period)]
                    sp = sp + data.loc[row_num, 'pwr_' + str(period)]
            if sp != 0.0:
                data.loc[row_num, 'acp_dominant_cycle'] = spx / sp

            # increase the display resolution by raising the normpwr to a higher mathematical power (optional)
            dominant_cycle_full_cycle = 0
            max_acp2 = 0.
            dominant_cycle_half_cycle = 0
            max_acp3 = 0.
            for period in range(8, acp_max+1):
                data.at[row_num, 'pwr_' + str(period)] = data.loc[row_num, 'pwr_' + str(period)] ** (2)
                # data.at[row_num, 'acp2_' + str(period)] = (-data.loc[row_num, 'acp_' + str(period)] + 1 )/2
                data.at[row_num, 'acp2_' + str(period)] = data.loc[row_num, 'acp_' + str(period)] ** (3)
                data.at[row_num, 'acp3_' + str(period)] = (data.loc[row_num, 'acp_' + str(period)] + 1 )/2
                data.at[row_num, 'acp3_' + str(period)] = data.loc[row_num, 'acp3_' + str(period)] ** (3)
                if data.loc[row_num, 'acp2_' + str(period)] > max_acp2:
                    dominant_cycle_full_cycle = period
                    max_acp2 = data.at[row_num, 'acp2_' + str(period)]
                if data.loc[row_num, 'acp2_' + str(period)] < max_acp3 :
                    dominant_cycle_half_cycle=period
                    max_acp3 = data.at[row_num, 'acp2_' + str(period)]
            data.at[row_num, 'acp_period_full_cycle'] = dominant_cycle_full_cycle
            data.at[row_num, 'acp2_strength'] = max_acp2
            data.at[row_num, 'acp_period_half_cycle'] = dominant_cycle_half_cycle
            data.at[row_num, 'acp3_strength'] = max_acp3
            if isna(dominant_cycle_full_cycle):
                dominant_cycle_full_cycle=0.0
            if isna(dominant_cycle_half_cycle):
                dominant_cycle_half_cycle=0.0
            if max_acp2 > -max_acp3:
                data.at[row_num, 'acp_aj_period'] = dominant_cycle_full_cycle * alpha2 + data.loc[row_num-1, 'acp_aj_period']*(1-alpha2)
            else:
                data.at[row_num, 'acp_aj_period'] = dominant_cycle_half_cycle * 2 * alpha2 + data.loc[row_num-1, 'acp_aj_period']*(1-alpha2)
            # data.at[row_num, 'acp_aj_period'] = data.loc[row_num-1, 'acp_aj_period']
        # my Period calcs
        # for row_num in range(max(2, avg_length), len(data)):
        #     if data.loc[row_num - 1, 'acp_1'] < data.loc[row_num, 'acp_1'] and \
        #             data.loc[row_num - 1, 'acp_1'] < data.loc[row_num - 2, 'acp_1']:
        #         data.at[row_num, 'acp_period'] = (row_num - last_period_row) * 2
        #         last_period_row = row_num
        #     else:
        #         data.at[row_num, 'acp_period'] = data.loc[row_num - 1, 'acp_period']
        #     data.at[row_num, 'acp_period_smooth'] = int((4 * data.loc[row_num, 'acp_period'] + 3 * data.loc[
        #         row_num - 1, 'acp_period'] + 2 * data.loc[row_num - 2, 'acp_period'] + data.loc[row_num - 3, 'acp_period']) / 10)
        #     *data.loc[row_num, 'acp_period']((4*data['acp_period']+ 3*data['acp_period'].shift(1)+2*data['acp_period'].shift(2)+data['acp_period'].shift(3))/10)
        # for period in range(2, acp_max+1):
        #     data['R1_' + str(period)] = data['R1_' + str(period)].fillna(0)
