#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

#Ehlers I1 and Q1

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_I1_Q1(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, destination=('i1','q1'), source='detrender', period='period'):
        print("Creating I1 Q1 Indicator")
        data[destination[0]]=data[source].shift(3)
        data[destination[0]]=data[destination[0]].fillna(0)
        data[destination[1]]=(data[source]*0.0962+data[source].shift(2)*0.5769-data[source].shift(4)*0.5769-data[source].shift(6)*0.0962)*(0.075*data[period]+0.54)
        data[destination[1]]=data[destination[1]].fillna(0)
