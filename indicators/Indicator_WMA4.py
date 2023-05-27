#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

#Ehlers Detrender

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_WMA4(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destination='wma4'):
        #1 bar of lag
        data[destination]=0
        data[destination]=(data[source]*4+data[source].shift(1)*3+data[source].shift(2)*2+data[source].shift(3))/10
        data[destination]=data[destination].fillna(0)
