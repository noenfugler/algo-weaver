#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp, sqrt
from math import isinf

class Indicator_Ehlers_Trend_Vigor(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destinations=['vigor', 'etv_trigger'], delta=0.2, period=10, trigger_lag=1):
        # delta = input(0.2, minval=0, title="delta")
        # period = input(20, minval=10, title="Cycle Period")
        # triggerLag = input(1, minval=11, title="Lag for trigger")
        # pi = 3.14
        beta = cos(2 * pi / period)
        gamma = 1 / cos(4 * pi * delta / period)
        alpha = gamma - (gamma * gamma - 1)**0.5
        data['_bp']=0.0
        data['_bp2']=0.0
        data['_signal']=0.0
        data['_power']=0.0
        data['_trend']=0.0
        half_period = round(period/2)
        quarter_period = round(period/4)
        a1 = exp(-sqrt(2) * pi / period)
        b1 = 2 * a1 * cos(sqrt(2) * pi / period)
        coef2 = b1
        coef3 = -a1 * a1
        coef1 = 1 - coef2 - coef3
        for row_num in range(self.min_warmup_candles,len(data)):
            # BP = 0.0
            data.at[row_num,'_bp']=0.5*(1-alpha) * (data.loc[row_num,source] - data.loc[row_num-2,source]) + beta * (1 + alpha) * data.loc[row_num-1,'_bp'] - alpha * data.loc[row_num-2,'_bp']
            # BP := 0.5 * (1 - alpha) * (close - nz(close[2]))                                  + beta * (1 + alpha) * nz(BP[1])                 - alpha * nz(BP[2])
            data.at[row_num,'_signal'] = data.loc[row_num,'_bp'] - data.loc[row_num-half_period,'_bp']
            # signal = (BP - nz(BP[round(period / 2)]))
            data.at[row_num,'_lead'] = 1.4 * (data.loc[row_num,'_bp'] - data.loc[row_num-quarter_period,'_bp'])
            # lead = 1.4 * (BP - nz(BP[round(period / 4)]))
            data.loc[row_num, '_bp2'] = data.loc[row_num,'_bp'] * data.loc[row_num,'_bp']
            # BP2 = BP * BP
            for j in range(0,period):
                data.at[row_num, '_power'] = data.loc[row_num, '_power'] + data.loc[row_num-j, '_bp2'] + data.loc[row_num-quarter_period-j, '_bp2']
            # power = sum(BP2, period) + sum(BP2[round(period / 4)], period)
            data.at[row_num, '_rms'] = (data.loc[row_num, '_power'] / period) ** 0.5
            # RMS = sqrt(power / period)
            data.at[row_num, '_ptop'] = 2 * 2**0.5 * data.loc[row_num, '_rms']
            # PtoP = 2 * sqrt(2) * RMS
            trend = 0.0
            data.at[row_num, '_trend'] = coef1 * (data.loc[row_num, source] - data.loc[row_num-period, source]) + coef2 * data.loc[row_num-1, '_trend'] + coef3 * data.loc[row_num-2, '_trend']
            # trend := coef1 * (close - nz(close[period])) + coef2 * nz(trend[1]) + coef3 * nz(trend[2])
            # // trend = xts(trend, order.by = index(x))
            data.at[row_num, '_tmp'] = data.loc[row_num, '_trend'] / data.loc[row_num, '_ptop']
            # tmp = trend / PtoP
            # // isintraday ? red: isdaily ? green: ismonthly ? blue: na
            if data.loc[row_num, '_tmp'] > 2:
                data.at[row_num, destinations[0]] = 2
            elif data.loc[row_num, '_tmp'] < -2:
                data.at[row_num, destinations[0]] = -2
            else:
                data.at[row_num, destinations[0]] = data.loc[row_num, '_tmp']
            # vigor = tmp > 2?2: tmp < -2?-2: tmp
            # // vigor[ is.na(vigor)] = 0
        data[destinations[1]] = data[destinations[0]].shift(trigger_lag)
            # trigger = vigor[triggerLag]