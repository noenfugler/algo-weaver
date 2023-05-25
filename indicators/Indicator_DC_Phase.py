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
from math import pi, cos, sin, atan, exp

class Indicator_DC_Phase(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, source='wma4'):
        slow_limit = 0.05
        self.df['dc_period'] = self.df['smooth_period'] + 0.5
        self.df['dc_period'] = self.df['dc_period'].apply(np.floor)
        self.df['real_part'] = 0.0
        self.df['imag_part'] = 0.0
        self.df['dc_phase'] = 0.0
        self.df['dc_phase_lead'] = 0.0
        self.df['sin_dc_phase'] = 0.0
        self.df['sin_dc_phase_lead'] = 0.0
        self.df['sin_dc_phase_smooth'] = 0.0
        self.df['sin_dc_phase_lead_smooth'] = 0.0
        self.df['itrend'] = 0.0
        self.df['detrender_smooth_last_peak'] = 0.0
        for row_num in range(0, len(self.df)):
            if row_num <= 2:
                self.df.at[row_num, 'detrender_smooth_last_peak'] = self.df['detrender_smooth'][row_num]
            else:
                if self.df['detrender_smooth'][row_num] < self.df['detrender_smooth'][row_num - 1] and self.df['detrender_smooth'][row_num - 1] > \
                        self.df['detrender_smooth'][row_num - 2]:
                    self.df.at[row_num, 'detrender_smooth_last_peak'] = self.df['detrender_smooth'][row_num - 1]
                else:
                    self.df.at[row_num, 'detrender_smooth_last_peak'] = self.df['detrender_smooth_last_peak'][row_num - 1]
            dc_period = self.df['dc_period'][row_num]
            real_part = 0.0
            imag_part = 0.0
            itrend = 0.0
            for count in range(0, min(int(dc_period), row_num)):
                real_part += cos(2 * pi * count / dc_period) * self.df[source][row_num - count]
                imag_part += sin(2 * pi * count / dc_period) * self.df[source][row_num - count]
                # itrend += self.df['price'][row_num-count]
            self.df.at[row_num, 'real_part'] = real_part
            self.df.at[row_num, 'imag_part'] = imag_part
            if abs(real_part) > 0.001:
                dc_phase = atan(imag_part / real_part)
            elif imag_part != 0.0:
                sign_imag_part = imag_part / abs(imag_part)
                dc_phase = pi / 2 * sign_imag_part
            else:
                dc_phase = pi / 2
            dc_phase = dc_phase + pi / 2
            # compensate for 1 bar lag of moving average
            dc_phase = dc_phase + 2 * pi / self.df['smooth_period'][row_num]

            if imag_part < 0:
                dc_phase += pi
            if dc_phase > (315 / 360) * 2 * pi:
                dc_phase -= 2 * pi
            self.df.at[row_num, 'dc_phase'] = dc_phase
            self.df.at[row_num, 'dc_phase_lead'] = dc_phase + pi / 4
            self.df.at[row_num, 'sin_dc_phase'] = sin(dc_phase)
            self.df.at[row_num, 'sin_dc_phase_lead'] = sin(dc_phase + pi / 4)

            # ORIGINAL ITREND CALCULATION
            # if dc_period > 0:
            #     itrend = itrend/dc_period

            # MODIFIED ITREND CALCULATION FROM PAGE 126
            int_period = int(self.cyc_part * self.df.loc[row_num, 'smooth_period'] + 0.5)
            for i in range(0, int_period):
                itrend = itrend + self.df.loc[row_num - i, 'price']
            if dc_period > 0:
                itrend = itrend / int_period
            self.df.at[row_num, 'itrend'] = itrend

        # def calc_

        # x = self.df[int_start_row:int_end_row]['I2']

        self.df['dc_phase_smooth'] = (4 * self.df['dc_phase'] + 3 * self.df['dc_phase'].shift(1) + 2 * self.df['dc_phase'].shift(2) + self.df[
            'dc_phase'].shift(3)) / 10
        self.df['sin_dc_phase_smooth'] = (4 * self.df['sin_dc_phase'] + 3 * self.df['sin_dc_phase'].shift(1) + 2 * self.df['sin_dc_phase'].shift(2) +
                                          self.df['sin_dc_phase'].shift(3)) / 10
        self.df['sin_dc_phase_lead_smooth'] = (4 * self.df['sin_dc_phase_lead'] + 3 * self.df['sin_dc_phase_lead'].shift(1) + 2 * self.df[
            'sin_dc_phase_lead'].shift(2) + self.df['sin_dc_phase_lead'].shift(3)) / 10
        self.df['trend_line'] = (4 * self.df['itrend'] + 3 * self.df['itrend'].shift(1) + 2 * self.df['itrend'].shift(2) + self.df['itrend'].shift(
            3)) / 10
        self.df['trend_line'] = self.df['trend_line'].fillna(0)
        self.df['trend_line_change_percent'] = self.df['trend_line'] / self.df['trend_line'].shift(1)
        self.df['trend_line_change_percent'] = self.df['trend_line_change_percent'].fillna(0)
        self.df['trend_line_first_derivative'] = self.df['trend_line'] - self.df['trend_line'].shift(1)
        self.df['trend_line_second_derivative'] = self.df['trend_line_first_derivative'] - self.df['trend_line_first_derivative'].shift(1)
