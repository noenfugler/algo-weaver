#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

#Detrended Ehlers Leading Indicator

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_Detrended_Ehlers_Leading_Indicator(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, period=14, destination1='deli'):
        prev_high = 0
        prev_low = 0
        alpha = 2 / (period + 1)
        data['deli'] = 0.0
        ema1 = 0.0
        ema2 = 0.0
        temp = 0.0
        for row_num in range(2, len(data)):
            if data.at[row_num - 1, 'high'] > data.at[row_num - 2, 'high']:
                prev_high = data.at[row_num - 1, 'high']
            if data.at[row_num - 1, 'low'] < data.at[row_num - 2, 'low']:
                prev_low = data.at[row_num - 1, 'low']
            price = (prev_high + prev_low) / 2
            alpha2 = alpha / 2
            ema1 = (alpha * price) + ((1 - alpha) * ema1)
            ema2 = ((alpha2) * price) + ((1 - alpha2) * ema2)
            dsp = ema1 - ema2
            temp = (alpha * dsp) + ((1 - alpha) * temp)
            data.at[row_num,'deli'] = dsp - temp

