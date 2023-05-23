from datasets.Dataset_class import Dataset

class Dataset_Binance_Futures_1h_1000_candles(Dataset):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super().__init__(kwargs)
        else:
            super().__init__()
        # self.warmup_candles=kwargs['warmup_candles']
        self.num_candles=1000
        self.date_split=False
        self.start_str = '2021-01-14'

    def load_data(self):
        self.data = self.exchange.get_klines(symbol=self.instrument.symbol, limit=self.num_candles+self.warmup_candles, utc=False, date_split=False, interval=self.interval, start_time=self.start_str)
        super(Dataset_Binance_Futures_1h_1000_candles, self).load_data()


