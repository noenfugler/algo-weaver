from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan
from math import isinf

class Indicator_percent_change(Indicator):
    def __init__(self):
        self.min_warmup_candles = 2

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destination='percent_change'):
        data[destination]=(data[source]/data[source].shift(1)-1.0)*100
        data[destination]=data[destination].fillna(0)
