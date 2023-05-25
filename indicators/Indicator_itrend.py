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

class Indicator_itrend(Indicator):
    def __init__(self):
        self.min_warmup_candles = 20

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='price', dest_itrend='itrend', dest_trigger='itrend_trigger', alpha=0.07):
        data[dest_itrend] = data[source]
        data[dest_trigger] = 0.0
        for row_num in range(3, len(data)):
            data.at[row_num, dest_itrend] = (alpha - (alpha ** 2) / 4) * data.loc[row_num, source] + 0.5 * alpha ** 2 * data.loc[
                row_num - 1, source] \
                                            - (alpha - 0.75 * alpha ** 2) * data.loc[row_num - 2, source] + 2 * (1 - alpha) * data.loc[
                                                row_num - 1, dest_itrend] \
                                            - (1 - alpha) ** 2 * data.loc[row_num - 2, dest_itrend]
            if row_num < 7:
                data.at[row_num, dest_itrend] = (data.loc[row_num, source] + 2 * data.loc[row_num - 1, source] + data.loc[
                    row_num - 2, source]) / 4
            data.at[row_num, dest_trigger] = 3 * data.loc[row_num, dest_itrend] - data.loc[row_num - 1, dest_itrend] - data.loc[
                row_num - 2, dest_itrend]

