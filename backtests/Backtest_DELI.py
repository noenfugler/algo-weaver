#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
# Detrended Ehlers Leading Indicator
from backtests.Backtest_class import Backtest
from strategies.Strategies import *
from instruments.Instruments import *
from exchanges.Exchange_Binance_Spot import Exchange_Binance_Spot
from datasets.Datasets import *
from graphs.Graphs import *
from communicators.telegram_communicator import *
from indicators.Indicators import *
from utils.util_functions import *
from configs.Config_class import *
from datetime import datetime, timedelta
from time import sleep


class Backtest_DELI(Backtest):
    def __init__(self, **kwargs):
        if len(kwargs)>0:
            super(Backtest_DELI, self).__init__(**kwargs)
        else:
            super(Backtest_DELI, self).__init__()

    def graph(self, save):
        # TODO: Move the assignment of the GRAPH to the Backtest initialization
        my_graph = Graph_DELI(strategy=self.strategy, save=save)
        image = my_graph.graph()
        return image

    def initialise(self, **kwargs):

        self.starting_cash=0
        self.trading_cash=0
        self.starting_position=1
        self.position = 1
        self.maximum_allocation=0.1

        self.exchange.initialise()


        self.strategy = Strategy_Do_Nothing(silent=False,allow_long=True, allow_short=False, bot=self)

        self.live=False

        indicator1 = Indicator_Detrended_Ehlers_Leading_Indicator()
        self.ls_indicators.append(indicator1)

        self.dataset = Dataset_Binance_Spot_250_candles(exchange=self.exchange, \
                                                                      live=False, \
                                                                      interval=self.interval, \
                                                                      warmup_candles=self.get_warmup_candles(), \
                                                                      instrument = self.instrument)
        self.dataset.load_data()

        indicator1.create(self.dataset.data)

def main():

    use_telegram=False

    config3 = Config(instrument=Instrument_ETHBTC(), interval='1d', wait_time=60, exchange=Exchange_Binance_Spot(), use_telegram=use_telegram)

    last_run = datetime.now()
    first_run = True
    wait_time = timedelta(minutes=config3.wait_time)
    my_telegram = Telegram_Communicator()
    my_backtest3 = Backtest_DELI(instrument=config3.instrument, interval=config3.interval, exchange=config3.exchange)

    while True:
        if (datetime.now() >= last_run + wait_time) or first_run:
            first_run = False
            last_run = datetime.now()
            last_run = round_time(last_run,timedelta(minutes=config3.wait_time), to='down')

            my_backtest3.initialise()
            my_backtest3.run()
            my_backtest3.report()

            image = my_backtest3.graph(config3.use_telegram)
            if config3.use_telegram:
                done=False
                fail_count=0
                while not done:
                    try:
                        my_telegram.send_graph(image)
                        done=True
                        print('Sent to Telegram.')
                    except:
                        print('Sending failed.')
                        fail_count+=1
                        sleep(2^fail_count)
                        if fail_count > 9:
                            done=True


        sleep(1)


if __name__ == "__main__":
    main()
