#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

import numpy as np

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan
from math import isinf

class Indicator_CCI_Adaptive(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destination_prefix='ccia', period='acp_aj_period', trend_angle=9, min_period=30, trigger_angle_trend = 0, mode='last'):
        # Correlate of one full cycle period
        self.set_up_super_smoother_parameters(ss_period=5)
        initial_length = int(self.min_warmup_candles/2)
        data[destination_prefix+'_real'] = 0.0
        data[destination_prefix+'_imag'] = 0.0
        data['ss_ccia_imag'] = 0.0
        data[destination_prefix+'_angle'] = 0.0
        data[destination_prefix+'_state'] = 0.0
        data[destination_prefix+'_amp'] = 0.0
        data[destination_prefix+'_correlator'] = 1.0
        data[destination_prefix+'_period'] = 6.0
        data[destination_prefix+'_period_aj'] = 60.0
        data[destination_prefix+'_mode_aj_intermediate'] = 0.0
        data[destination_prefix+'_mode_aj'] = 0.0
        data[destination_prefix+'_cycle_count'] = 0.0
        if mode=='last':
            length = int(data.loc[len(data)-1, period])
            start_length=length
        elif mode=='highly':
            start_length = initial_length
        for row_num in range(start_length, len(data)):
            Sx = 0.0
            Sy = 0.0
            Sxx = 0.0
            Sxy = 0.0
            Syy = 0.0

            if mode=='highly':
                if np.isnan(data.loc[row_num, period]):
                    length = 20
                else:
                    length = int(data.loc[row_num, period])

            for count in range(1, length +1):
                X = data.loc[row_num -(count -1) ,source]
                Y = cos( 2 *pi *(count -1) / length)
                Sx = Sx + X
                Sy = Sy + Y
                Sxx = Sxx + X * X
                Sxy = Sxy + X * Y
                Syy = Syy + Y * Y
            if (length * Sxx - Sx * Sx > 0) and (length * Syy - Sy * Sy > 0):
                data.at[row_num, destination_prefix+'_real'] = (length * Sxy - Sx * Sy) / ((length * Sxx - Sx * Sx) * (length * Syy - Sy * Sy)) ** (1 / 2)
            Sx = 0.0
            Sy = 0.0
            Sxx = 0.0
            Sxy = 0.0
            Syy = 0.0
            for count in range(1, length + 1):
                X = data.loc[row_num - (count - 1), source]
                Y = -sin(2 * pi * (count - 1) / length)
                Sx = Sx + X
                Sy = Sy + Y
                Sxx = Sxx + X * X
                Sxy = Sxy + X * Y
                Syy = Syy + Y * Y
            if (length * Sxx - Sx * Sx > 0) and (length * Syy - Sy * Sy > 0):
                data.at[row_num, destination_prefix+'_imag'] = (length * Sxy - Sx * Sy) / ((length * Sxx - Sx * Sx) * (length * Syy - Sy * Sy)) ** (1 / 2)
            # Compute the angle as an arctangent function and resolve ambiguity
            if data.loc[row_num, destination_prefix+'_imag'] != 0:
                data.loc[row_num, destination_prefix+'_angle'] = pi / 2 + atan(data.loc[row_num, destination_prefix+'_real'] / data.loc[row_num, destination_prefix+'_imag'])
            if data.loc[row_num, destination_prefix+'_imag'] > 0:
                data.at[row_num, destination_prefix+'_angle'] = data.loc[row_num, destination_prefix+'_angle'] - pi
            # Do not allow the rate change of angle to go negative
            if data.loc[row_num - 1, destination_prefix+'_angle'] - data.loc[row_num, destination_prefix+'_angle'] < 3 * pi / 2 and data.loc[row_num, destination_prefix+'_angle'] < data.loc[
                row_num - 1, destination_prefix+'_angle']:
                data.at[row_num, destination_prefix+'_angle'] = data.loc[row_num - 1, destination_prefix+'_angle']
            if abs(data.loc[row_num, destination_prefix+'_angle'] - data.loc[row_num - 1, destination_prefix+'_angle']) < trend_angle / 180 * pi and (
                    data.loc[row_num, destination_prefix+'_angle'] < trigger_angle_trend or data.loc[row_num, destination_prefix+'_angle'] > pi + trigger_angle_trend):
                data.at[row_num, destination_prefix+'_state'] = -1
            elif abs(data.loc[row_num, destination_prefix+'_angle'] - data.loc[row_num - 1, destination_prefix+'_angle']) < trend_angle / 180 * pi and (
                    data.loc[row_num, destination_prefix+'_angle'] >= trigger_angle_trend and data.loc[row_num, destination_prefix+'_angle'] <= pi + trigger_angle_trend):
                data.at[row_num, destination_prefix+'_state'] = 1
            if data.loc[row_num, destination_prefix+'_state'] == 1:
                data.at[row_num, destination_prefix+'_correlator'] = data.loc[row_num - 1, destination_prefix+'_correlator'] * 1.01
            elif data.loc[row_num, destination_prefix+'_state'] == -1:
                data.at[row_num, destination_prefix+'_correlator'] = data.loc[row_num - 1, destination_prefix+'_correlator'] / 1.01
            else:
                data.at[row_num, destination_prefix+'_correlator'] = data.loc[row_num - 1, destination_prefix+'_correlator']
            if (data.loc[row_num, destination_prefix+'_angle'] - data.loc[row_num - 1, destination_prefix+'_angle']) != 0:
                data.at[row_num, destination_prefix+'_period'] = 2 * pi / (data.loc[row_num, destination_prefix+'_angle'] - data.loc[row_num - 1, destination_prefix+'_angle'])
            else:
                data.at[row_num, destination_prefix+'_period'] = data.at[row_num - 1, destination_prefix+'_period']
            # data.at[row_num,destination_prefix+'_period'] = min(data.at[row_num,destination_prefix+'_period'],min_period)
            data.at[row_num, destination_prefix+'_amp'] = (data.loc[row_num, destination_prefix+'_real'] ** 2 + data.loc[row_num, destination_prefix+'_imag'] ** 2) ** (1 / 2)
            # data.at[row_num, 'ss_conv_all'] = self.ss_c1 * (data.loc[row_num, 'conv_all'] + data.loc[row_num - 1, 'conv_all']) / 2 + self.ss_c2 * data.loc[row_num - 1, 'ss_conv_all'] + self.ss_c3 * data.loc[row_num - 2, 'ss_conv_all']
            data.at[row_num, 'ss_ccia_imag'] = self.ss_c1 * (data.loc[row_num, destination_prefix+'_imag'] + data.loc[row_num - 1, destination_prefix+'_imag']) / 2 + self.ss_c2 * data.loc[row_num - 1, 'ss_ccia_imag'] + self.ss_c3 * data.loc[row_num - 2, 'ss_ccia_imag']
            data.at[row_num,destination_prefix+'_angle_roc']=data.loc[row_num,destination_prefix+'_angle']-data.loc[row_num-1,destination_prefix+'_angle']
            if data.loc[row_num,destination_prefix+'_angle_roc'] < -pi :
                data.at[row_num, destination_prefix+'_angle_roc'] = data.loc[row_num, destination_prefix+'_angle_roc']+ 2*pi
            data.at[row_num,destination_prefix+'_period_aj']=2*pi/data.loc[row_num, destination_prefix+'_angle_roc']
            if isinf(data.at[row_num,destination_prefix+'_period_aj']) or data.at[row_num,destination_prefix+'_period_aj']> 40:
                #trend mode
                if data.at[row_num,destination_prefix+'_imag'] > data.at[row_num,destination_prefix+'_real']:
                    data.at[row_num, destination_prefix+'_mode_aj_intermediate']=-1
                else:
                    data.at[row_num, destination_prefix+'_mode_aj_intermediate']=1
            else:
                #cycle mode
                data.at[row_num, destination_prefix+'_mode_aj_intermediate'] = 0
            # data.at[row_num, destination_prefix+'_mode_aj']=data.loc[row_num, destination_prefix+'_mode_aj_intermediate']
            data.at[row_num, destination_prefix+'_mode_aj']=(data.loc[row_num, destination_prefix+'_mode_aj_intermediate']+data.loc[row_num-1, destination_prefix+'_mode_aj_intermediate'])/2
            if data.loc[row_num, destination_prefix+'_mode_aj']<1 and data.loc[row_num, destination_prefix+'_mode_aj']>-1:
                data.at[row_num, destination_prefix+'_mode_aj']=0

            # else:
            #     data.at[row_num, destination_prefix+'_mode_aj'] = data.loc[row_num-1, destination_prefix+'_mode_aj_intermediate']
            if data.loc[row_num, destination_prefix+'_imag'] > data.loc[row_num, destination_prefix+'_real'] and \
                    data.loc[row_num-1, destination_prefix+'_imag'] < data.loc[row_num-1, destination_prefix+'_real'] or \
                    data.loc[row_num, destination_prefix+'_imag'] < data.loc[row_num, destination_prefix+'_real'] and \
                    data.loc[row_num - 1, destination_prefix+'_imag'] > data.loc[row_num - 1, destination_prefix+'_real']:
                data.at[row_num, destination_prefix+'_cycle_count']=1
            else:
                data.at[row_num, destination_prefix+'_cycle_count'] = data.loc[row_num-1, destination_prefix+'_cycle_count']+1
        data[destination_prefix+'_gap']=data[destination_prefix+'_real']-data[destination_prefix+'_imag']

