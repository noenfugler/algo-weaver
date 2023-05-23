#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
from math import pi, exp, cos

class Indicator():
    def __init__(self):
        # if df is None:
        #     raise Exception('must pass in a dataframe')
        # self.df = df
        self.min_warmup_candles = None

    def initialise(self, data, warmup_candles):
        #create indicator over warmup candle number of rows in dataset
        pass

    def set_up_super_smoother_parameters(self,ss_period=10):
        self.ss_a = exp(-1.414*pi/ss_period)
        self.ss_b = 2 * self.ss_a * cos(1.414 * pi / ss_period)
        self.ss_c2 = self.ss_b
        self.ss_c3 = -self.ss_a * self.ss_a
        self.ss_c1 = 1 - self.ss_c2 - self.ss_c3

    # def set_up_super_smoother_parameters(self,ss_period=10):
    #     self.ss_a = exp(-1.414*pi/ss_period)
    #     self.ss_b = 2 * self.ss_a * cos(1.414 * pi/2 / ss_period)
    #     self.ss_c2 = self.ss_b
    #     self.ss_c3 = -self.ss_a * self.ss_a
    #     self.ss_c1 = 1 - self.ss_c2 - self.ss_c3
