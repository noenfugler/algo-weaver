from instruments.Instrument_class import Instrument

class Instrument_ETHBTC(Instrument):
    def __init__(self):
        self.buying = 'ETH'
        self.using = 'BTC'
        self.symbol = 'ETHBTC'
