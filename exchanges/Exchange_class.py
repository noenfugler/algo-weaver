#    This file is part of Algo-weaver.
#    Algo-weaver is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
#    License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
#    later version.
#    Algo-weaver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#    details.
#    You should have received a copy of the GNU General Public License along with Algo-weaver. If not, see
#    <https://www.gnu.org/licenses/>.
class Exchange():
    def __init__(self, **kwargs):
        print('Creating exchange object')
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

    def initialise(self):
        # Initialise the connection to the exchange.
        # Returns: none
        pass

    def get_account_balance(self, symbol='USDT'):
        # call the exchange to get the account balance.  Define
        # Accepts:  Symbol = the symbol of the currency to get the balance for
        # Returns: float
        pass

    def get_open_orders(self):
        # call the exchange to get the open orders.
        pass
