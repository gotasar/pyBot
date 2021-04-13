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
        user_name = message['message']['chat']['username']

        if 'text' not in message['message']:
            bot.send_message(user_id, f"Опять за старое взялся? {user_name}!", reply_markup=BotKeyboard.start_keyboard())
            return

        text = message['message']['text']

        if '/start' == text:
            pass
        elif 'Начать тест' in message:
            pass
        elif 'Статистика' in message:
            pass
        elif 'Настройка параметров' in message:
            pass
        elif 'Увеличить сложность' in message:
            pass
        elif 'Уменьшить сложность' in message:
            pass
        elif 'Увеличить повторения' in message:
            pass
        elif 'Уменьшить повторения' in message:
            pass
        elif 'Сменить тему' in message:
            pass
        elif 'Тема: ' in message:
            pass
        elif 'Ответ:' in message:
            bot.send_message(user_id, f"Я получил ответ", reply_markup=BotKeyboard.start_keyboard())
            pass

        # Echo test without logic
        print(f"{bot} {text} {user_id}")
        bot.send_message(user_id, f"Эхо: {text}", reply_markup=BotKeyboard.start_keyboard())
        text = generate_test_question(conn, user_id)
        bot.send_message(user_id, f"Тестовый вопрос: {text}", reply_markup=BotKeyboard.start_keyboard())


