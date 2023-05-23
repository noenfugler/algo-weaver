from instruments.Instrument_class import Instrument

class Instrument_ETHUSDT(Instrument):
    def __init__(self):
        self.buying = 'ETH'
        self.using = 'USDT'
        self.symbol = 'ETHUSDT'
