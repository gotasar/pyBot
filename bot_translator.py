from tb_static import TB
from db_static import DB

bot = TB.get()
conn = DB.get()

from bot_logic import generate_test_question

class bot_translator:
    @staticmethod
    def processing(message):
        user_id = message['message']['chat']['id']
        text = message['message']['text']
        # Echo test without logic
        print(f"{bot} {text} {user_id}")
        bot.send_message(user_id, f"Эхо: {text}", reply_markup=start_keyboard())
        text = generate_test_question(conn, user_id)
        bot.send_message(user_id, f"Тестовый вопрос: {text}", reply_markup=start_keyboard())
        pass


#def send_message(bot_d, txt):
#    pass


#def test(bot_d, message):
#    pass


from telebot import types
def start_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn_start = types.KeyboardButton('Начать тест')
    btn_statistic = types.KeyboardButton('Статистика')
    btn_params = types.KeyboardButton('Настройка параметров')
    markup.add(btn_start)
    markup.add(btn_statistic)
    markup.add(btn_params)
    return markup