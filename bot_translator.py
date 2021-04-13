from tb_static import TB
from db_static import DB

bot = TB.bot()
conn = DB.conn()


class bot_translator:
    @staticmethod
    def processing(message):
        user_id = message['message']['chat']['id']
        print(bot)
        #bot.send_message(user_id, "Опять за старое взялся?")
        pass


def send_message(bot_d, txt):
    pass


def test(bot_d, message):
    pass
