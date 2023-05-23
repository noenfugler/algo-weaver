from strategies.Strategy_class import Strategy
from orders.Order_class import Order

class Strategy_CCI_imag_and_mama_long_only(Strategy):

    def should_long_setup_trigger(self):
        last_row = len(self.bot.data)
        if self.bot.data.loc[last_row - 1, 'cci_imag'] > self.bot.data.loc[last_row - 2, 'cci_imag'] and \
                self.bot.data.loc[last_row - 3, 'cci_imag'] > self.bot.data.loc[last_row - 2, 'cci_imag']:
            #trough.  set trigger
            self.long_trigger = True
            self.modify_long_trigger = False

    def should_long(self):
        last_row = len(self.bot.data)
        if self.bot.position > 0:
            return False
        elif self.long_trigger:
            return self.bot.data.loc[last_row-1, 'mama'] > self.bot.data.loc[last_row-2, 'mama']
        else:
            return False

    def should_modify_long_setup_trigger(self):
        last_row = len(self.bot.data)
        if self.bot.data.loc[last_row - 1, 'cci_imag'] < self.bot.data.loc[last_row - 2, 'cci_imag'] and \
                self.bot.data.loc[last_row - 3, 'cci_imag'] < self.bot.data.loc[last_row - 2, 'cci_imag']:
            #peak.  set trigger
            self.modify_long_trigger = True
            self.long_trigger = False

    def should_modify_long(self):
        last_row = len(self.bot.data)
        if self.bot.position <= 0:
            return False
        else:
            if self.bot.data.loc[last_row-1, 'cci_angle_roc']==0:
                return self.bot.data.loc[last_row - 1, 'cci_real'] < self.bot.data.loc[last_row-1, 'cci_imag']
                # return True
            else:
                return self.bot.data.loc[last_row - 1, 'cci_imag'] < self.bot.data.loc[last_row-1, 'cci_real']

    def should_short(self):
        return False

    def should_modify_short(self):
        return False

    def go_long(self):
        self.long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = self.bot.trading_cash / self.bot.get_last_close()
        this_order.create_order(symbol=self.bot.instrument.symbol, side="BUY", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    def modify_long(self):
        self.modify_long_trigger=False
        this_order = Order()
        print('datetime=',self.bot.get_last_datetime())
        print('close=', self.bot.get_last_close())
        quantity = -self.bot.position
        this_order.create_order(symbol=self.bot.instrument.symbol, side="SELL", type="MARKET", exchange=self.bot.exchange, quantity=quantity, bot=self.bot, timestamp=self.bot.get_last_datetime())
        return this_order

    def go_short(self):
        return None

    def modify_short(self):
        return None

    def graph(self):
        self.bot.data_active = self.bot.data #.iloc[self.get_warmup_candles():]
        fig, axs = plt.subplots(3, figsize=(15, 9.5))
        fig.suptitle(self.interval + ' CCI BTCAUD' + str(self.bot.data_active['date_time'].tail(1).values[0][:19]))
        axs[0].set_yscale('log')
        # axs[0].set_ylim(50000,80000)
        line1 = axs[0].plot(self.bot.data_active['date_time'], self.bot.data_active['close'],color='black', linewidth=0.75)
        line1 = axs[0].plot(self.bot.data_active['date_time'], self.bot.data_active['ss_mama'],color='green', linewidth=0.75)

        axs2=axs[0].twinx()
        line1 = axs2.plot(self.bot.data['date_time'], self.bot.data['cci_mode_aj'],color='purple', linewidth=0.75)
        line4 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_imag'],color='red', linewidth=0.75)
        line5 = axs[1].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_real'],color='blue', linewidth=0.75)
        axs[2].set_ylim(0,50)
        line = axs[2].plot(self.bot.data_active['date_time'], self.bot.data_active['cci_period_aj'],color='red', linewidth=0.75)

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.bot.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs[0].plot(buy_x, buy_y, '^', color='blue', markersize=7)
        axs[0].plot(sell_x, sell_y, 'v', color='red', markersize=7)

        plt.show()

    def graph_single(self):
        fig, axs = plt.subplots(1, figsize=(15, 9.5))
        fig.suptitle(self.bot.interval + ' CCI BTCAUD' + str(self.bot.data['date_time'].tail(1).values[0][:19]))
        axs.set_yscale('log')
        line1 = axs.plot(self.bot.data['date_time'], self.bot.data['close'],color='black', linewidth=0.75)
        line1 = axs.plot(self.bot.data['date_time'], self.bot.data['ss_mama'],color='green', linewidth=0.75)
        # line2 = axs[1].plot(self.bot.data['date_time'], self.bot.data['cci_angle'],color='black', linewidth=0.75)
        # line3 = axs[1].plot(self.bot.data['date_time'], self.bot.data['cci_state'],color='blue', linewidth=0.75)
        axs2=axs.twinx()
        line4 = axs2.plot(self.bot.data['date_time'], self.bot.data['cci_imag'],color='red', linewidth=0.75)
        line5 = axs2.plot(self.bot.data['date_time'], self.bot.data['cci_real'],color='blue', linewidth=0.75)
        # axs[1].set_yscale('log')
        # line4 = axs[1].plot(self.bot.data['date_time'], self.bot.data['cci_period'],color='green', linewidth=0.75)
        # axs3 = axs[1].twinx()
        # line4 = axs3.plot(self.bot.data['date_time'], self.bot.data['cci_angle_roc'],color='black', linewidth=0.75)

        # buy and sell plots
        buy_x = []
        buy_y = []
        sell_x = []
        sell_y = []
        for index, t in enumerate(self.bot.ls_trades):
            if t.side == "BUY":
                buy_x.append(t.timestamp)
                buy_y.append(t.price)
            elif t.side == 'SELL':
                sell_x.append(t.timestamp)
                sell_y.append(t.price)

        axs.plot(buy_x, buy_y, '^', color='blue', markersize=7)
        axs.plot(sell_x, sell_y, 'v', color='red', markersize=7)

        plt.show()



