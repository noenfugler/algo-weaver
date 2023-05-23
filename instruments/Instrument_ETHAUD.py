from instruments.Instrument_class import Instrument

class Instrument_ETHAUD(Instrument):
    def __init__(self):
        self.buying = 'ETH'
        self.using = 'AUD'
        self.symbol = 'ETHAUD'
