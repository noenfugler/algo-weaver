from instruments.Instrument_class import Instrument

class Instrument_BCHUSDT(Instrument):
    def __init__(self):
        self.buying = 'BCH'
        self.using = 'USDT'
        self.symbol = 'BCHUSDT'
