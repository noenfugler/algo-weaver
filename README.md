# Welcome to Algo-weaver
Algo-weaver is a algorithmic trading platform written in Python.  This code is licensed under

## Inputs
### Exchanges
Exchanges are both sources of price data and destinations to execute trades
At the moment, the only exhcanges set up are Binance Futures and Binance Spot.  These have not been tested recently.

### Instruments
Instruments are pairs drawn from exchanges.  examples are ETHUSDT, which is an Etherium/USDT pair.  An instrument file begins with Instrument_ and defines a class with a parent class of "Instrument".




Algo-weaver utilizes candle data called datasets.  Each dataset is a combination of a data source, a period and a number of candles

