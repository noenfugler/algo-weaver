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
from math import pi, cos, sin, atan
from math import isinf

class Indicator_CCI(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', period=20, trend_angle=9, min_period=30, trigger_angle_trend = 0):
        # Correlate of one full cycle period
        self.set_up_super_smoother_parameters(ss_period=5)
        length =period
        data['cci_real'] = 0.0
        data['cci_imag'] = 0.0
        data['ss_cci_imag'] = 0.0
        data['cci_angle'] = 0.0
        data['cci_state'] = 0.0
        data['cci_amp'] = 0.0
        data['cci_correlator'] = 1.0
        data['cci_period'] = 6.0
        data['cci_period_aj'] = 60.0
        data['cci_mode_aj_intermediate'] = 0.0
        data['cci_mode_aj'] = 0.0
        for row_num in range(length, len(data)):
            Sx = 0.0
            Sy = 0.0
            Sxx = 0.0
            Sxy = 0.0
            Syy = 0.0
            for count in range(1, length +1):
                X = data.loc[row_num -(count -1) ,source]
                Y = cos( 2 *pi *(count -1) / period)
                Sx = Sx + X
                Sy = Sy + Y
                Sxx = Sxx + X * X
                Sxy = Sxy + X * Y
                Syy = Syy + Y * Y
            if (length * Sxx - Sx * Sx > 0) and (length * Syy - Sy * Sy > 0):
                data.at[row_num, 'cci_real'] = (length * Sxy - Sx * Sy) / ((length * Sxx - Sx * Sx) * (length * Syy - Sy * Sy)) ** (1 / 2)
            Sx = 0.0
            Sy = 0.0
            Sxx = 0.0
            Sxy = 0.0
            Syy = 0.0
            for count in range(1, length + 1):
                X = data.loc[row_num - (count - 1), source]
                Y = -sin(2 * pi * (count - 1) / period)
                Sx = Sx + X
                Sy = Sy + Y
                Sxx = Sxx + X * X
                Sxy = Sxy + X * Y
                Syy = Syy + Y * Y
            if (length * Sxx - Sx * Sx > 0) and (length * Syy - Sy * Sy > 0):
                data.at[row_num, 'cci_imag'] = (length * Sxy - Sx * Sy) / ((length * Sxx - Sx * Sx) * (length * Syy - Sy * Sy)) ** (1 / 2)
            # Compute the angle as an arctangent function and resolve ambiguity
            if data.loc[row_num, 'cci_imag'] != 0:
                data.loc[row_num, 'cci_angle'] = pi / 2 + atan(data.loc[row_num, 'cci_real'] / data.loc[row_num, 'cci_imag'])
            if data.loc[row_num, 'cci_imag'] > 0:
                data.at[row_num, 'cci_angle'] = data.loc[row_num, 'cci_angle'] - pi
            # Do not allow the rate change of angle to go negative
            if data.loc[row_num - 1, 'cci_angle'] - data.loc[row_num, 'cci_angle'] < 3 * pi / 2 and data.loc[row_num, 'cci_angle'] < data.loc[
                row_num - 1, 'cci_angle']:
                data.at[row_num, 'cci_angle'] = data.loc[row_num - 1, 'cci_angle']
            if abs(data.loc[row_num, 'cci_angle'] - data.loc[row_num - 1, 'cci_angle']) < trend_angle / 180 * pi and (
                    data.loc[row_num, 'cci_angle'] < trigger_angle_trend or data.loc[row_num, 'cci_angle'] > pi + trigger_angle_trend):
                data.at[row_num, 'cci_state'] = -1
            elif abs(data.loc[row_num, 'cci_angle'] - data.loc[row_num - 1, 'cci_angle']) < trend_angle / 180 * pi and (
                    data.loc[row_num, 'cci_angle'] >= trigger_angle_trend and data.loc[row_num, 'cci_angle'] <= pi + trigger_angle_trend):
                data.at[row_num, 'cci_state'] = 1
            if data.loc[row_num, 'cci_state'] == 1:
                data.at[row_num, 'cci_correlator'] = data.loc[row_num - 1, 'cci_correlator'] * 1.01
            elif data.loc[row_num, 'cci_state'] == -1:
                data.at[row_num, 'cci_correlator'] = data.loc[row_num - 1, 'cci_correlator'] / 1.01
            else:
                data.at[row_num, 'cci_correlator'] = data.loc[row_num - 1, 'cci_correlator']
            if (data.loc[row_num, 'cci_angle'] - data.loc[row_num - 1, 'cci_angle']) != 0:
                data.at[row_num, 'cci_period'] = 2 * pi / (data.loc[row_num, 'cci_angle'] - data.loc[row_num - 1, 'cci_angle'])
            else:
                data.at[row_num, 'cci_period'] = data.at[row_num - 1, 'cci_period']
            # data.at[row_num,'cci_period'] = min(data.at[row_num,'cci_period'],min_period)
            data.at[row_num, 'cci_amp'] = (data.loc[row_num, 'cci_real'] ** 2 + data.loc[row_num, 'cci_imag'] ** 2) ** (1 / 2)
            # data.at[row_num, 'ss_conv_all'] = self.ss_c1 * (data.loc[row_num, 'conv_all'] + data.loc[row_num - 1, 'conv_all']) / 2 + self.ss_c2 * data.loc[row_num - 1, 'ss_conv_all'] + self.ss_c3 * data.loc[row_num - 2, 'ss_conv_all']
            data.at[row_num, 'ss_cci_imag'] = self.ss_c1 * (data.loc[row_num, 'cci_imag'] + data.loc[row_num - 1, 'cci_imag']) / 2 + self.ss_c2 * data.loc[row_num - 1, 'ss_cci_imag'] + self.ss_c3 * data.loc[row_num - 2, 'ss_cci_imag']
            data.at[row_num,'cci_angle_roc']=data.loc[row_num,'cci_angle']-data.loc[row_num-1,'cci_angle']
            if data.loc[row_num,'cci_angle_roc'] < -pi :
                data.at[row_num, 'cci_angle_roc'] = data.loc[row_num, 'cci_angle_roc']+ 2*pi
            data.at[row_num,'cci_period_aj']=2*pi/data.loc[row_num, 'cci_angle_roc']
            if isinf(data.at[row_num,'cci_period_aj']) or data.at[row_num,'cci_period_aj']> 40:
                #trend mode
                if data.at[row_num,'cci_imag'] > data.at[row_num,'cci_real']:
                    data.at[row_num, 'cci_mode_aj_intermediate']=-1
                else:
                    data.at[row_num, 'cci_mode_aj_intermediate']=1
            else:
                #cycle mode
                data.at[row_num, 'cci_mode_aj_intermediate'] = 0
            # data.at[row_num, 'cci_mode_aj']=data.loc[row_num, 'cci_mode_aj_intermediate']
            data.at[row_num, 'cci_mode_aj']=(data.loc[row_num, 'cci_mode_aj_intermediate']+data.loc[row_num-1, 'cci_mode_aj_intermediate'])/2
            if data.loc[row_num, 'cci_mode_aj']<1 and data.loc[row_num, 'cci_mode_aj']>-1:
                data.at[row_num, 'cci_mode_aj']=0

            # else:
            #     data.at[row_num, 'cci_mode_aj'] = data.loc[row_num-1, 'cci_mode_aj_intermediate']
        data['cci_gap']=data['cci_real']-data['cci_imag']

