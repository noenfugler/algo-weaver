from indicators.Indicator_class import Indicator
from math import pi, cos, sin, atan
from math import isinf

class Indicator_Trend_AJ(Indicator):
    def __init__(self):
        self.min_warmup_candles = 50

    def initialise(self, kwargs):
        self.create(kwargs)

    def create(self, data, source='price', period1='cci_period_aj', period2='period', destination='trend_aj', short_period_cycle_fraction=0.1):
        # Correlate of one full cycle period
        # self.set_up_super_smoother_parameters(ss_period=5)
        length = 50
        data[destination] = 0.0
        # start_candle_num = max(data.loc[0:100, 'period'])
        for row_num in range(length, len(data)):
            if isinf(data.loc[row_num,period1]):
                long_period=40
                data.loc[row_num,period2]
                # short_period=10
            else:
                long_period=data.loc[row_num, period1]
            short_period=max(int(long_period*short_period_cycle_fraction),1)
            average_long = sum(data.loc[row_num-long_period:row_num, source])/len(data.loc[row_num-long_period:row_num, source])
            data.at[row_num,'aj_avg_long']=average_long
            # average_short = sum(data.loc[row_num-short_period:row_num, source])/len(data.loc[row_num-short_period:row_num, source])
            average_short = data.loc[row_num, source]
            data.loc[row_num,destination] = (average_short/average_long)-1

