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
