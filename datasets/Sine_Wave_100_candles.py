from datasets.Dataset_class import Dataset
import pandas as pd
from math import sin, pi

class Dataset_Sine_Wave_100_Candles(Dataset):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super().__init__(**kwargs)
        else:
            super().__init__(**kwargs)
        self.num_candles=250
        self.date_split=False
        # self.start_str = '2021-05-01'

    def load_data(self, period=20., long_period = 42., amplitude_short=1., amplitude_long=0):
        self.data = pd.DataFrame()

        for row_num in range(0,self.num_candles):
            self.data.loc[row_num, 'short_date_time'] = str(100000000000+row_num)
            self.data.loc[row_num, 'date_time'] = str(10000000000000+row_num)
            self.data.loc[row_num, 'open']  = amplitude_short * sin((row_num - 0.5) / period * 2 * pi)       + sin(row_num / long_period * 2 * pi) * amplitude_long + (amplitude_short+amplitude_long) * 1.1
            self.data.loc[row_num, 'close'] = amplitude_short * sin((row_num + 0.5) / period * 2 * pi)       + sin(row_num / long_period * 2 * pi) * amplitude_long + (amplitude_short+amplitude_long) * 1.1
            self.data.loc[row_num, 'high']  = amplitude_short * sin((row_num)       / period * 2 * pi) * 1.1 + sin(row_num / long_period * 2 * pi) * amplitude_long + (amplitude_short+amplitude_long) * 1.1
            self.data.loc[row_num, 'low']   = amplitude_short * sin((row_num)       / period * 2 * pi) / 1.1 + sin(row_num / long_period * 2 * pi) * amplitude_long + (amplitude_short+amplitude_long) * 1.1


