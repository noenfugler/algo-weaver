#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Alog-weaver. If not, see
#    <https://www.gnu.org/licenses/>.

from datasets.Dataset_class import Dataset

class Dataset_Binance_Spot_100_candles(Dataset):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super().__init__(**kwargs)
        else:
            super().__init__()
        self.num_candles=100
        self.date_split=False
        self.start_str = '2021-07-03'

    def load_data(self):
        self.data = self.exchange.get_klines(symbol=self.instrument.symbol, limit=100, utc=False, date_split=False, interval=self.interval, start_time=self.start_str)
        super(Dataset_Binance_Spot_100_candles, self).load_data()


