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
