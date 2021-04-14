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

        if 'message' not in message:
            return

        user_id = message['message']['chat']['id']

        if 'username' not in message['message']['chat']:
            return

        user_name = message['message']['chat']['username']

        if 'text' not in message['message']:
            bot.send_message(user_id, f"Опять за старое взялся? {user_name}!", reply_markup=BotKeyboard.start_keyboard())
            return

        text = message['message']['text']


        if '/start' == text:
            pass
        elif 'Начать тест' == text:
            start_test(conn, user_id)
            pass
        elif 'Статистика' == text:
            get_statistic(conn, user_id)
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
            answer_processing(conn, user_id, text)
            print(f"oTVET {bot} {text} {user_id}")
            #bot.send_message(user_id, f"Я получил ответ", reply_markup=BotKeyboard.start_keyboard())
        else:
            # Echo test without logic
            print(f"{bot} {text} {user_id}")
            bot.send_message(user_id, f"Эхо: {text}", reply_markup=BotKeyboard.start_keyboard())
            text = generate_test_question(conn, user_id)
            bot.send_message(user_id, f"Тестовый вопрос: {text}", reply_markup=BotKeyboard.start_keyboard())
            # delete_all_progress_users(conn)


def delete_all_progress_users(conn):
    curr = conn.cursor()
    curr.execute("DELETE FROM users")
    curr.execute("DELETE FROM progress")
    conn.commit()


def start_test(conn, user_id):
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET num_questions = 1 WHERE id = {user_id} ")
    generate_question(conn, user_id)
    conn.commit()


def stop_test(conn, user_id):
    cur = conn.cursor()
    cur.execute(f"SELECT rating, max_question FROM users WHERE id = {user_id}")
    row = cur.fetchone()
    if row is None:
        return

    bot.send_message(user_id, f"Тест завершен")
    bot.send_message(user_id, f"Правильность на {row[0]} из {row[1]}", reply_markup=BotKeyboard.start_keyboard())

    cur.execute(f"UPDATE users SET num_questions = 1 WHERE id = {user_id} ")
    generate_question(conn, user_id)
    conn.commit()


def answer_processing(conn, user_id, text):
    cur = conn.cursor()
    cur.execute(f'SELECT num_questions, max_question FROM users WHERE id = {user_id}')
    row = cur.fetchone()

    if row is None:
        return

    if f'{row[0]}. Ответ: ' not in text:
        return

    words = text.split(f'{row[0]}. Ответ: ')
    print(words)
    words = words[1].split(': ')
    print(words)
    res = check_answer(conn, user_id, words[0], words[1])
    # bot.send_message(user_id, res, reply_markup=BotKeyboard.start_keyboard())

    if row[0] == row[1]:
        bot.send_message(user_id, res, reply_markup=BotKeyboard.start_keyboard())
    else:
        num_add(conn, user_id, 1)
        bot.send_message(user_id, res)
        generate_question(conn, user_id)


def num_add(conn, user_id, delta):
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET num_questions = num_questions + {delta} WHERE id = {user_id} ")
    conn.commit()


def generate_question(conn, user_id):
    q = generate_test_question(conn, user_id)
    if q != -1:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        print(q)
        for options in q["Answer options"]:
            markup.add(types.KeyboardButton(options))
        bot.send_message(user_id, q["Question"], reply_markup=markup)


def check_answer(conn, user_id, word_en, word_ru):
    curr = conn.cursor()
    curr.execute(f"SELECT id, word FROM users WHERE id = {user_id}")
    row_user = curr.fetchone()
    res = ''

    # если пользователь найден
    if row_user is not None:
        curr.execute(f"SELECT id FROM words WHERE en = '{word_en}' AND ru = '{word_ru}'")
        row_word = curr.fetchone()
        # если слово найдено в таблице
        if row_word is not None:
            res = "Красавчик"
            print("Красавчик")
            curr.execute(
                f"UPDATE progress SET grade = grade + 1, rating = rating + 1 WHERE user_id = {row_user[0]} AND word = {row_word[0]}")

        else:
            res = "Нетушки"

            # Reset progress en word
            curr.execute(f"SELECT id FROM words WHERE en = '{word_en}'")
            row_word = curr.fetchone()
            if row_word is None:
                return
            curr.execute(
                f"UPDATE progress SET grade = 0 WHERE user_id = {row_user[0]} AND word = {row_word[0]}")

            # Reset progress ru word
            curr.execute(f"SELECT id FROM words WHERE ru = '{word_ru}'")
            row_word = curr.fetchone()
            if row_word is None:
                return
            curr.execute(
                f"UPDATE progress SET grade = 0 WHERE user_id = {row_user[0]} AND word = {row_word[0]}")

    conn.commit()
    return res


def get_statistic(conn, user_id):
    curr = conn.cursor()
    curr.execute('SELECT users.id, users.first_name, users.grade, ' +
                 'themes.theme, AVG(progress.grade) AS avg_progress_grade ' +
                 'FROM users ' +
                 f'INNER JOIN progress ON progress.user_id = {user_id} ' +
                 'INNER JOIN words ON words.id = progress.word ' +
                 'INNER JOIN themes ON themes.id = words.theme ' +
                 f'WHERE users.id = {user_id} '
                 f'GROUP BY users.id, users.first_name, users.grade, themes.theme ')
    row = curr.fetchone()
    if row is None:
        return
    bot.send_message(user_id, f'Пользователь: {row[1]}', reply_markup=BotKeyboard.start_keyboard())
    bot.send_message(user_id, f'Тема: {row[3]}  — {"{0:.2f}".format(row[4] / row[2] * 100)} %',
                     reply_markup=BotKeyboard.start_keyboard())
    print(f'Тема: {row[3]}  — {"{0:.2f}".format(row[4] / row[2] * 100)} %')
    for row in curr:
        print(f'Пользователь: {row[1]}')
        bot.send_message(user_id, f'Тема: {row[3]}  — {"{0:.2f}".format(row[4]/row[2] * 100) } %',
                         reply_markup=BotKeyboard.start_keyboard())



