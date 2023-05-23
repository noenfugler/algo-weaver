class Exchange():
    def __init__(self, **kwargs):
        self.min_leverage = None
        self.max_leverage = None
        self.default_leverage = None
        self.api_key = None
        self.secret_key = None
        self.taker_fee = None
        self.maker_fee = None
        self.live = None
        self.can_short = None
        # self.bot = kwargs['bot']