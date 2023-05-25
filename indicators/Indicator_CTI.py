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

class Indicator_CTI(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destinations=['cti_long','cti_short','cti_trend','cti_correlator','pc_cti_long'], lperiod=40, speriod=10):
        # Correlate of one full cycle period
        # length=period
        # data['cci_real']=0.0
        # data['cci_imag']=0.0
        # data['cci_angle']=0.0
        # data['cci_state']=0.0
        data[destinations[0]] = 0.0
        data[destinations[1]] = 0.0
        data[destinations[2]] = -0.5
        data[destinations[3]] = 1.0
        # data[destinations[4]] = 0.0
        for row_num in range(lperiod, len(data)):
            Sx = 0.0
            Sy = 0.0
            Sxx = 0.0
            Sxy = 0.0
            Syy = 0.0
            for count in range(1, lperiod + 1):
                # X = data.loc[row_num-(count-1),'price']
                # X = data.loc[row_num-(count-1),'zero_lag']
                # X = data.loc[row_num-(count-1),'trend_line']
                X = data.loc[row_num - (count - 1), source]
                Y = -count
                # Y = - count ** (1/2)
                Sx = Sx + X
                Sy = Sy + Y
                Sxx = Sxx + X * X
                Sxy = Sxy + X * Y
                Syy = Syy + Y * Y
            if (lperiod * Sxx - Sx * Sx > 0) and (lperiod * Syy - Sy * Sy > 0):
                data.at[row_num, destinations[0]] = (lperiod * Sxy - Sx * Sy) / ((lperiod * Sxx - Sx * Sx) * (lperiod * Syy - Sy * Sy)) ** (1 / 2)
            Sx = 0.0
            Sy = 0.0
            Sxx = 0.0
            Sxy = 0.0
            Syy = 0.0
            # speriod = int(data.loc[row_num,'period'])
            for count in range(1, speriod + 1):
                # X = data.loc[row_num-(count-1),'price']
                # X = data.loc[row_num-(count-1),'zero_lag']
                # X = data.loc[row_num-(count-1),'trend_line']
                X = data.loc[row_num - (count - 1), source]
                # Y = -sin(2*pi*(count -1) / period)
                Y = - count
                # Y = - (1/2) ** count
                Sx = Sx + X
                Sy = Sy + Y
                Sxx = Sxx + X * X
                Sxy = Sxy + X * Y
                Syy = Syy + Y * Y
            if (speriod * Sxx - Sx * Sx > 0) and (speriod * Syy - Sy * Sy > 0):
                data.at[row_num, destinations[1]] = (speriod * Sxy - Sx * Sy) / ((speriod * Sxx - Sx * Sx) * (speriod * Syy - Sy * Sy)) ** (1 / 2)
            # if data.loc[row_num,destinations[0]] > 0.5 : #and data.loc[row_num,destinations[0]] > 0.5:
            if data.loc[row_num, destinations[1]] > data.loc[row_num, destinations[0]]:  # and data.loc[row_num,destinations[0]] > 0.5:
                data.at[row_num, destinations[2]] = 1
            # elif data.loc[row_num,destinations[0]] < -0.5 :# and data.loc[row_num,destinations[0]] < -0.5:
            elif data.loc[row_num, destinations[1]] < data.loc[row_num, destinations[0]]:  # and data.loc[row_num,destinations[0]] > 0.5:
                data.at[row_num, destinations[2]] = -1
            else:
                data.at[row_num, destinations[2]] = 0
            if data.loc[row_num, destinations[2]] == 1:
                data.at[row_num, destinations[3]] = data.loc[row_num - 1, destinations[3]] * 1.01
            elif data.loc[row_num, destinations[2]] == -1:
                data.at[row_num, destinations[3]] = data.loc[row_num - 1, destinations[3]] / 1.01
            else:
                data.at[row_num, destinations[3]] = data.loc[row_num - 1, destinations[3]]
        data[destinations[4]] = (data[destinations[0]]+1)/(data[destinations[0]].shift(1)+1)-1

