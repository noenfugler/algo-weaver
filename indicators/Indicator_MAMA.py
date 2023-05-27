#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
#Ehlers MAMA and FAMA indicators

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_MAMA(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, destination=('mama','fama'),sources=('close','i1'), ss_period=10):
        print("Creating MAMA Indicator")
        fast_limit = 0.5
        slow_limit = 0.05
        data['phase'] = 0.0
        data['delta_phase'] = 0.0
        data[destination[0]] = data[sources[0]]
        data[destination[1]] = data[sources[0]]
        data['ss_mama'] = data[sources[0]]
        data['ss_fama'] = data[sources[0]]
        ss_a = exp(-1.414 * pi / ss_period)
        ss_b = 2 * ss_a * cos(1.414 * pi / 2 / ss_period)
        ss_c2 = ss_b
        ss_c3 = -ss_a * ss_a
        ss_c1 = 1 - ss_c2 - ss_c3

        for row_num in range(2, len(data)):
            if data.loc[row_num, sources[1]] != 0:
                data.at[row_num, 'phase'] = atan(data.loc[row_num, 'q1'] / data.loc[row_num, sources[1]])
            data.at[row_num, 'delta_phase'] = atan(data.loc[row_num - 1, 'phase'] - data.loc[row_num, 'phase'])
            if data.loc[row_num, 'delta_phase'] < 1:
                data.at[row_num, 'delta_phase'] = 1.0
            data.at[row_num, 'alpha'] = fast_limit / data.loc[row_num, 'delta_phase']
            if data.loc[row_num, 'alpha'] < slow_limit:
                data.at[row_num, 'alpha'] = slow_limit
            data.at[row_num, destination[0]] = data.loc[row_num, 'alpha'] * data.loc[row_num, sources[0]] + (1 - data.loc[row_num, 'alpha']) * \
                                          data.loc[row_num - 1, destination[0]]
            data.at[row_num, destination[1]] = 0.5 * data.loc[row_num, 'alpha'] * data.loc[row_num, destination[0]] + (
                        1 - 0.5 * data.loc[row_num, 'alpha']) * data.loc[row_num - 1, destination[1]]
            data.at[row_num, 'ss_mama'] = ss_c1 * (data.loc[row_num, destination[0]] + data.loc[row_num - 1, destination[0]]) / 2 + ss_c2 * data.loc[
                row_num - 1, 'ss_mama'] + ss_c3 * data.loc[row_num - 2, 'ss_mama']
            data.at[row_num, 'ss_fama'] = ss_c1 * (data.loc[row_num, destination[1]] + data.loc[row_num - 1, destination[1]]) / 2 + ss_c2 * data.loc[
                row_num - 1, 'ss_fama'] + ss_c3 * data.loc[row_num - 2, 'ss_fama']
