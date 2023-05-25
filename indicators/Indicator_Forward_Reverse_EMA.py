#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

# {
#     Forward / Reverse
# EMA
# (c)
# 2017
# John
# F.Ehlers
# }
#
# Inputs:
# AA(.1);
#
# Vars:
# CC(.9),
# RE1(0),
# RE2(0),
# RE3(0),
# RE4(0),
# RE5(0),
# RE6(0),
# RE7(0),
# RE8(0),
# EMA(0),
# Signal(0);
#
# CC = 1 - AA;
# EMA = AA * Close + CC * EMA[1];
#
# RE1 = CC * EMA + EMA[1];
# RE2 = Power(CC, 2) * RE1 + RE1[1];
# RE3 = Power(CC, 4) * RE2 + RE2[1];
# RE4 = Power(CC, 8) * RE3 + RE3[1];
# RE5 = Power(CC, 16) * RE4 + RE4[1];
# RE6 = Power(CC, 32) * RE5 + RE5[1];
# RE7 = Power(CC, 64) * RE6 + RE6[1];
# RE8 = Power(CC, 128) * RE7 + RE7[1];
#
# Signal = EMA - AA * RE8;
#
# Plot1(Signal);
# Plot2(0);


from indicators.Indicator_class import Indicator

import math

class Indicator_Forward_Reverse_EMA(Indicator):
    def create(self, source='price', alpha=0.1):
        pass