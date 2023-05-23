#Ehlers Super Smother

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_Super_Smoother(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, source='close', destination='ss_close', ss_period=5):
        data[source]=data[source].fillna(0)
        data[destination]=data[source]
        self.set_up_super_smoother_parameters(ss_period=ss_period)
        for row_num in range(2, len(data)):
            data.at[row_num, destination] = self.ss_c1 * (data.loc[row_num, source] + data.loc[row_num - 1, source]) / 2 \
                                           + self.ss_c2 * data.loc[row_num - 1, destination] + self.ss_c3 * data.loc[row_num - 2, destination];
