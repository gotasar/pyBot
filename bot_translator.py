from tb_static import TB
from db_static import DB
from bot_logic import generate_test_question
from bot_keyboard import BotKeyboard
from telebot import types

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
            generate_question(conn, user_id)
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


def answer_processing(conn, user_id, text):
    cur = conn.cursor()
    cur.execute(f'SELECT num_questions FROM users WHERE = {user_id}')
    row = cur.fetchone()

    if f'{row[0]}. Ответ: ' not in text:
        return

    words = text.split(f'{row[0]}. Ответ: ')
    words = words.split(': ')


def generate_question(conn, user_id):
    q = generate_test_question(conn, user_id)
    if q != -1:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        print(q)
        for options in q["Answer options"]:
            markup.add(types.KeyboardButton(options))
        bot.send_message(user_id, q["Question"], reply_markup=markup)
