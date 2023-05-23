#Ehlers Detrender

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_Detrender(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, destination='detrender', source='wma4', period='period'):
        data[destination] = (data[source]*0.0962+data[source].shift(2)*0.5769-data[source].shift(4)*0.5769-data[source].shift(6)*0.0962)*(0.075*data[period].shift(1)+0.54)
        data[destination] = data[destination].fillna(0)
        data[destination] = (4 * data[destination] + 3* data[destination].shift(1) + 2* data[destination].shift(2) + data[destination].shift(3))/10
