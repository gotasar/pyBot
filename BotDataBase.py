# web: gunicorn app:app
# worker: python main.py 5000
# heroku addons:create heroku-postgresql:hobby-dev
# Created postgresql-metric-65240 as DATABASE_URL
# pip install psycopg2-binary

import os
import psycopg2


class BotDataBase:
    conn = -1
    cur = -1

    @staticmethod
    def connect():
        DATABASE_URL = os.environ['postgresql-metric-65240']
        #BotDataBase.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        BotDataBase.conn = psycopg2.connect(database="dds7sqrcoqeb9d",
                                            user="pyelnnrkmnqscq",
                                            password="923bf537fb88e9ea583ee915f4efc2d778c8ec277e400fe12d3315787a6e310d",
                                            host="ec2-52-6-178-202.compute-1.amazonaws.com",
                                            port=5432)
        BotDataBase.cur = BotDataBase.conn.cursor()
        pass

    @staticmethod
    def tb_users():
        BotDataBase.cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, " +
                                "login VARCHAR(64), state INTEGER," +
                                "theme INTEGER," +
                                "complexity INTEGER," +
                                "grade INTEGER," +
                                "num_questions INTEGER)")
        BotDataBase.conn.commit()


