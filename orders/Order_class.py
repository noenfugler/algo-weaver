#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
from trades.Trade_class import Trade

class Order():
    def __init__(self):
        self.symbol = None
        self.side = None                # ["Buy", "Sell"]
        self.positionSide = None        # implement later  Default BOTH for One-way Mode ; LONG or SHORT for Hedge Mode. It must be sent in Hedge Mode.
        self.type = None                # ["LIMIT", "MARKET", "STOP", "TAKE_PROFIT", "STOP_MARKET", "TAKE_PROFIT_MARKET", "TRAILING_STOP_MARKET"]
        self.timeInForce = None         # implement later
        self.quantity = 0.0            # Cannot be sent with closePosition=true(Close-All)
        self.reduceOnly = None          # "true" or "false". default "false". Cannot be sent in Hedge Mode; cannot be sent with closePosition=true
        self.stopPrice = None           # Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.
        self.closePosition = None       # true, false；Close-All，used with STOP_MARKET or TAKE_PROFIT_MARKET.
        self.activationPrice = None     # Used with TRAILING_STOP_MARKET orders, default as the latest price(supporting different workingType)
        self.callbackRate = None        # Used with TRAILING_STOP_MARKET orders, min 0.1, max 5 where 1 for 1%
        self.workingType = None         # stopPrice triggered by: "MARK_PRICE", "CONTRACT_PRICE". Default "CONTRACT_PRICE"
        self.priceProtect = None        # "TRUE" or "FALSE", default "FALSE". Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders.
        self.newOrderRespType = None    # "ACK", "RESULT", default "ACK"
        self.recvWindow = None          #
        self.timestamp = None           #

    def __str__(self):
        return "timestamp : % s, " \
               "price : % s, " \
               "quatity : % s" % (self.timestamp, self.candle_open, self.quantity)

    def create_limit(self, side, quantity, reduce_only, symbol):
        self.type="LIMIT"
        self.side = side
        self.quantity = quantity
        self.reduceOnly = reduce_only
        self.symbol = symbol
        self.create_order()

    def create_market(self, side, quantity, symbol):
        self.type="MARKET"
        self.side = side
        self.quantity = quantity
        self.symbol = symbol
        self.create_order()

    def fulfill(self, timestamp, price):
        if self.type=="MARKET":
            return Trade(symbol=self.symbol, timestamp=timestamp, bot=self.bot, side=self.side, exchange=self.exchange, price=price, quantity=self.quantity)

    def create_order(self, **kwargs):
        if 'symbol' in kwargs:
            self.symbol = kwargs['symbol']
        else:
            raise Exception('Must pass in a symbol')

        if 'timestamp' in kwargs:
            self.timestamp = kwargs['timestamp']
        else:
            raise Exception('Must pass in a timestamp')

        if 'bot' in kwargs:
            self.bot = kwargs['bot']
        else:
            raise Exception('Must pass in a bot')

        if 'side' in kwargs:
            self.side = kwargs['side']
        else:
            raise Exception('Must pass in an side')

        if 'type' in kwargs:
            self.type = kwargs['type']
        else:
            raise Exception('Must pass in an type')

        if 'exchange' in kwargs:
            self.exchange = kwargs['exchange']
        else:
            raise Exception('Must pass in an exchange object')

        if 'stopPrice' in kwargs:
            self.stopPrice = kwargs['stopPrice']

        if 'closePosition' in kwargs:
            self.closePosition = kwargs['closePosition']

        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity']
        else:
            raise Exception('Must pass a quantity')

        if self.type=='STOP_MARKET':
            if (self.stopPrice == 0.0 or self.closePosition==''):
                raise Exception('STOP MARKET must have STOP PRICE and CLOSE POSITION')
            else:
                if self.bot.live:
                    self.exchange.client.futures_create_order(symbol=symbol, side=side, type=type, stopPrice=stopPrice, closePosition=closePosition)
                else:
                    self.fulfilled = True
                    self.fulfilled_price = self.bot.get_last_close()  #TODO: Will need to be reworked when trades are created.  Just a stopgap at the moment
                    self.fulfilled_time = self.timestamp
                    print('DUMMY ORDER', 'symbol=', self.symbol, 'side=', self.side, 'type=', self.type, 'stop price=', self.stopPrice, 'close position=', self.closePosition)

        elif (self.type=="MARKET"):
            if self.quantity==0.0:
                raise Exception('BUY and SELL order require quantity')
            else:
                if self.bot.live:
                    self.exchange.client.futures_create_order(symbol=symbol, side=side, type=type, quantity=quantity)
                else:
                    self.fulfilled = True
                    self.fulfilled_price = self.bot.get_last_open()  #TODO: Will need to be reworked when trades are created.  Just a stop-gap at the moment
                    self.fulfilled_time = self.timestamp
                    print('DUMMY ORDER', 'symbol=', self.symbol, 'side=', self.side, 'type=', self.type, 'quantity=', self.quantity, 'price=', self.fulfilled_price)

        self.candle_open = self.bot.get_last_open()
