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
        elif 'Начать тест' == text:
            pass
        elif 'Статистика' == text:
            pass
        elif 'Настройка параметров' == text:
            pass
        elif 'Увеличить сложность' == text:
            pass
        elif 'Уменьшить сложность' == text:
            pass
        elif 'Увеличить повторения' == text:
            pass
        elif 'Уменьшить повторения' == text:
            pass
        elif 'Сменить тему' == text:
            pass
        elif 'Тема: ' in text:
            pass
        elif 'Ответ: ' in text:
            print(f"oTVET {bot} {text} {user_id}")
            bot.send_message(user_id, f"Я получил ответ", reply_markup=BotKeyboard.start_keyboard())
            pass

        # Echo test without logic
        print(f"{bot} {text} {user_id}")
        bot.send_message(user_id, f"Эхо: {text}", reply_markup=BotKeyboard.start_keyboard())
        text = generate_test_question(conn, user_id)
        bot.send_message(user_id, f"Тестовый вопрос: {text}", reply_markup=BotKeyboard.start_keyboard())


