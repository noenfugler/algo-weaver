from instruments.Instrument_class import Instrument

class Instrument_BTCAUD(Instrument):
    def __init__(self):
        self.buying = 'BTC'
        self.using = 'AUD'
        self.symbol = 'BTCAUD'
