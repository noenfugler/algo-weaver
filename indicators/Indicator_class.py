from math import pi, exp, cos

class Indicator():
    def __init__(self):
        # if df is None:
        #     raise Exception('must pass in a dataframe')
        # self.df = df
        self.min_warmup_candles = None

    def initialise(self, data, warmup_candles):
        #create indicator over warmup candle number of rows in dataset
        pass

    def set_up_super_smoother_parameters(self,ss_period=10):
        self.ss_a = exp(-1.414*pi/ss_period)
        self.ss_b = 2 * self.ss_a * cos(1.414 * pi / ss_period)
        self.ss_c2 = self.ss_b
        self.ss_c3 = -self.ss_a * self.ss_a
        self.ss_c1 = 1 - self.ss_c2 - self.ss_c3

    # def set_up_super_smoother_parameters(self,ss_period=10):
    #     self.ss_a = exp(-1.414*pi/ss_period)
    #     self.ss_b = 2 * self.ss_a * cos(1.414 * pi/2 / ss_period)
    #     self.ss_c2 = self.ss_b
    #     self.ss_c3 = -self.ss_a * self.ss_a
    #     self.ss_c1 = 1 - self.ss_c2 - self.ss_c3
