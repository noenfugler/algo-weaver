#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from strategies.Strategy_class import Strategy
from orders.Order_class import Order
import matplotlib.pyplot as plt
from math import isinf


class Strategy_Do_Nothing(Strategy):

    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Strategy_Do_Nothing, self).__init__(kwargs)

    def should_long(self):
        return False

    def should_modify_long(self):
        return False

    def should_short(self):
        return False

    def should_modify_short(self):
        return False

    def go_long(self):
        return None

    def modify_long(self):
        return None

    def go_short(self):
        return None

    def modify_short(self):
        return None

    def graph(self):
        pass
