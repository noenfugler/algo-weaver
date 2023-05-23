# http://thepythoncorner.com/dev/how-create-telegram-bot-in-Python/
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api

import telegram
pass
class Telegram_Communicator():
    def __init__(self):
        self.TELEGRAM_BOT_TOKEN = 'Add Telegram Bot Token Here'
        self.TELEGRAM_CHAT_ID = 'Add Telegram Chat ID Here'
        # PHOTO_PATH = '../chart_output/Figure_1.png'


    def send_graph(self, photo_path):
        # bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="From Bot")
        self.bot = telegram.Bot(token=self.TELEGRAM_BOT_TOKEN)
        self.bot.send_photo(chat_id=self.TELEGRAM_CHAT_ID, photo=open(photo_path, 'rb'))

