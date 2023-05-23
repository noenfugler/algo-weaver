from datasets.Dataset_class import Dataset

class Dataset_Binance_Futures_1h_100_candles(Dataset):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super().__init__(**kwargs)
        else:
            super().__init__()
        self.num_candles=100
        self.date_split=False
        self.start_str = '2021-06-06'

    def load_data(self):
        self.data = self.exchange.get_klines(symbol=self.instrument.symbol, limit=100, utc=False, date_split=False, interval=self.interval, start_time=self.start_str)
        super(Dataset_Binance_Futures_1h_100_candles, self).load_data()


