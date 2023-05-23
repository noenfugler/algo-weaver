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
        self.df[destination]=0
        self.df[destination]=(self.df[source]*4+self.df[source].shift(1)*3+self.df[source].shift(2)*2+self.df[source].shift(3))/10
        self.df[destination]=self.df[destination].fillna(0)
