from instruments.Instrument_class import Instrument

class Instrument_AUDUSDT(Instrument):
    def __init__(self):
        self.buying = 'AUD'
        self.using = 'USDT'
        self.symbol = 'AUDUSDT'
