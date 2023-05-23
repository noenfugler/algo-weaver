from instruments.Instrument_class import Instrument

class Instrument_BTCUSDT(Instrument):
    def __init__(self):
        self.buying = 'BTC'
        self.using = 'USDT'
        self.symbol = 'BTCUSDT'
