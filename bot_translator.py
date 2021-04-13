from tb_static import TB
from db_static import DB
from bot_logic import generate_test_question
from bot_keyboard import BotKeyboard

bot = TB.get()
conn = DB.get()


class bot_translator:
    @staticmethod
    def processing(message):
        user_id = message['message']['chat']['id']
        text = message['message']['text']
        # Echo test without logic
        print(f"{bot} {text} {user_id}")
        bot.send_message(user_id, f"Эхо: {text}", reply_markup=BotKeyboard.start_keyboard())
        text = generate_test_question(conn, user_id)
        bot.send_message(user_id, f"Тестовый вопрос: {text}", reply_markup=BotKeyboard.start_keyboard())

