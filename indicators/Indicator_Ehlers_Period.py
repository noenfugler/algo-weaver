#Ehlers Autocorrelation Filter indicator

from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan, exp

class Indicator_Ehlers_Period(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, **kwargs):
        self.create(kwargs)

    def create(self, data, source1='wma4', source_re='Re', source_im='Im', destination1='period', destination2='smooth_period'):
        last_period = 0.0
        last_smooth_period = 0.0
        period = 0.0
        for index_label, row_series in data.iterrows():
            if row_series[source_re]!=0 and row_series[source_im]!=0:
                period = pi/atan(row_series[source_im]/row_series[source_re])
            if period!=0 and period > 1.5 * last_period:
                period = 1.5 * last_period
            if period != 0 and period < 0.67 * last_period:
                period = 0.67 * last_period
            if period < 6:
                period = 6
            if period > 50:
                period = 50
            period = 0.2 * period + 0.8 * last_period
            smooth_period = 0.33 * period + 0.67 * last_smooth_period
            data.at[index_label, destination1] = period
            data.at[index_label, destination2] = smooth_period
            last_period = period
            last_smooth_period = smooth_period
