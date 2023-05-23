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
from math import pi, cos, sin, atan, exp

class Indicator_BSW(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', bsw_duration=40):
        # HighPass filter cyclic components whose periods are shorter than Duration input
        alpha1 = (1 - sin(2 * pi / bsw_duration)) / cos(2 * pi / bsw_duration)
        a1 = exp(-1.414 * pi / 10)
        b1 = 2 * a1 * cos(1.414 * pi / 10)
        c2 = b1
        c3 = -a1 * a1
        c1 = 1 - c2 - c3
        data['bsw_filt'] = 0.0
        data['HP'] = 0.0
        for row_num in range(2, len(data)):
            data.at[row_num, 'HP'] = 0.5 * (1 + alpha1) * (data.loc[row_num, source] - data.loc[row_num - 1, source]) + alpha1 * \
                                        data.loc[row_num - 1, 'HP']
            # Smooth with a Super Smoother Filter from equation 3-3
            data.at[row_num, 'bsw_filt'] = c1 * (data.loc[row_num, 'HP'] + data.loc[row_num - 1, 'HP']) / 2 + \
                                              c2 * data.loc[row_num - 1, 'bsw_filt'] + c3 * data.loc[row_num - 2, 'bsw_filt']
        # 3 Bar average of Wave amplitude and power
        data['wave'] = (data['bsw_filt'] + data['bsw_filt'].shift(1) + data['bsw_filt'].shift(2)) / 3
        data['pwr'] = (data['bsw_filt'] ** 2 + data['bsw_filt'].shift(1) ** 2 + data['bsw_filt'].shift(2) ** 2) / 3
        # Normalize the Average Wave to Square Root of the Average Power
        data['bs_wave'] = data['wave'] / data['pwr'] ** (1 / 2)
        data['bs_wave_smoothed'] = (data['bs_wave'] + data['bs_wave'].shift(1) + data['bs_wave'].shift(2) + data['bs_wave'].shift(3) + \
                                       data['bs_wave'].shift(4) + data['bs_wave'].shift(5) + data['bs_wave'].shift(6)) / 7

        # data['bsw_cycle_mode'] = 1
        # data.loc[data['bs_wave'] < 0, 'bsw_cycle_mode'] = -1
        
