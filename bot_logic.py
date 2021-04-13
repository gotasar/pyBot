import random

from tb_static import TB
from db_static import DB

bot = TB.get()
conn = DB.get()


def generate_test_question(conn, user_id):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user_row = cur.fetchone()
    # Найти слова по теме
    words = get_words(user_row)
    if words == -1:
        return -1
    # Создать вопрос и варианты ответов
    random.shuffle(words)
    index = 0
    o = []
    grade = user_row[5]
    complexity = user_row[4]
    for word in words:
        index += 1
        if word["grade"] < grade:
            q = f"Переведите: {word['EN']}"
            o.append(f"{word['EN']}: {word['RU']}")
            i = 1
            while i < complexity:
                o.append(f"{word['EN']}: {words[(index + i + 2) % len(words)]['RU']}")
                i += 1
            random.shuffle(o)
            res = {"Question": q, "Answer options": o}
            return res
    else:
        return -1


def get_words(user_row):
    print(user_row)
    if user_row is None:
        return -1
    theme = user_row[3]
    words = []
    cur = conn.cursor()
    cur.execute(f"SELECT en, ru FROM words WHERE theme = {theme}")
    for row in cur:
        words.append({'EN': row[0], 'RU': row[1]})
    return words