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
from math import pi, cos, sin, atan
from math import isinf

class Indicator_price(Indicator):
    def __init__(self):
        self.min_warmup_candles = 1

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, sources=['close'], destination='price'):
        data[destination]=0.0
        for source in sources:
            data[destination] = data[destination] + data[source]
        data[destination] = data[destination] / len(sources)
