#Ehlers I1 and Q1

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_I1_Q1(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, destination=('i1','q1'), source='detrender', period='period'):
        data[destination[0]]=data[source].shift(3)
        data[destination[0]]=data[destination[0]].fillna(0)
        data[destination[1]]=(data[source]*0.0962+data[source].shift(2)*0.5769-data[source].shift(4)*0.5769-data[source].shift(6)*0.0962)*(0.075*data[period]+0.54)
        data[destination[1]]=data[destination[1]].fillna(0)
