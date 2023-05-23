class Config():
    def __init__(self, **kwargs):
        self.instrument = kwargs['instrument']
        self.interval = kwargs['interval']
        self.wait_time = kwargs['wait_time']
        self.exchange = kwargs['exchange']
        self.use_telegram = kwargs['use_telegram']