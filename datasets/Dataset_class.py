#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
class Dataset():
    def __init__(self, **kwargs):
        # for key, value in kwargs.items():
        #     val = value
        #     if isinstance(val, dict):
        #         val = MyClass(**val)
        #     setattr(self, key, val)
        #exchange - exchange object
        #live - boolean to indicate whether backtesting or live trading
        #interval - candle interval
        #end_datetime, start_datetime, num_candles.  Require 2 of the three or if only num_candles, assume end_datetime is last candle.
        #warmup_candles - candles to warm up indicators.  Not to be backtested.
        if 'exchange' not in kwargs:
            raise Exception('must pass in an Exchange object (exchange)')
        else:
            self.exchange = kwargs['exchange']
        if 'live' not in kwargs:
            raise Exception("must pass in parameter as a boolean (live)")
        else:
            self.live = kwargs['live']
        if 'interval' not in kwargs:
            raise Exception('must pass in a valid interval (interval)')
        else:
            if kwargs['interval'] not in ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']:
                raise Exception('must pass in a valid interval (interval) : ' + "['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']")
            else:
                self.interval = kwargs['interval']
        if 'end_datetime' in kwargs and 'num_candles' in kwargs:
            self.num_candles = kwargs['num_candles']
            pass
        elif 'start_datetime' in kwargs and 'num_candles' in kwargs:
            self.num_candles = kwargs['num_candles']
            pass
        elif 'start_datetime' in kwargs and 'end_datetime' in kwargs:
            pass
        elif 'num_candles' in kwargs:
            if isinstance(kwargs['num_candles'],int):
                self.num_candles = kwargs['num_candles']
                if not self.live:
                    self.end_datetime = self.work_out_last_candle()
                else:
                    pass
            else:
                raise Exception("must pass in an interger number of candles (num_candles)")

            pass #assume end date is now

        if 'instrument' in kwargs:
            self.instrument = kwargs['instrument']
        else:
            raise Exception("must pass in an instrument (instrument)")
        self.data=None
        self.finished = False
        self.warmup_candles = kwargs['warmup_candles']
        self.current_candle = self.warmup_candles + 1


    # def new_data(self):
    #     #used to query whether new data has arrived from the dataset
    #     temp = self.new_data
    #     self.new_data = False
    #     return temp

    def initialise(self):
        # self.load_data()
        pass

    # def finished(self):
        #method which returns True when dataset has been fully served (i.e. last row already given).  Only for backtest trading.
        # pass

    def get_next_candle(self):
        #query database class to get data.   Database class should handle getting any missing data from exchange.
        #return data in a df
        #also return a boolean indicating whether the last candle has been served previously
        #return False, self.new_df

        if self.finished:
            raise Exception('Check whether dataset is finished!')
        result=self.data.loc[0:self.current_candle]
        self.current_candle +=1
        if self.current_candle >= len(self.data):
            self.finished = True
        return result

    def get_num_candles(self):
        return len(self.data)

    def work_out_last_candle(self):
        #when passed only num_candles, assume end_datetime is last candle.
        #TODO: Is this required????  Couldn't we just query the exchange without a start or end?
        pass

    def get_last_close(self):
        return float(self.data.iloc[-1]['close'])

    def load_data(self):
        # for indicator in self.ls_indicators:
        #     indicator.create()
        pass


    def finished(self):
        return self.finished