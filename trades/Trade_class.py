#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
#TODO: Trade is just a copy of Order at the moment.  Make it what it needs to be.

class Trade():
    def __init__(self, **kwargs):


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

        if 'exchange' in kwargs:
            self.exchange = kwargs['exchange']
        else:
            raise Exception('Must pass in an exchange object')

        if 'price' in kwargs:
            self.price = kwargs['price']
        else:
            raise Exception('Must pass in an price')

        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity']
        else:
            raise Exception('Must pass a quantity')

        if 'bot' in kwargs:
            self.bot = kwargs['bot']
        else:
            raise Exception('Must pass a bot')

        self.bot.position += self.quantity
        self.bot.trading_cash -= self.quantity*self.price


    def __str__(self):
        return "timestamp : % s, " \
               "price : % s, " \
               "quantity : % s" % (self.timestamp, self.price, self.quantity)

    # def create_order(self, **kwargs):

