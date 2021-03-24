# web: gunicorn app:app
# worker: python main.py 5000
# heroku addons:create heroku-postgresql:hobby-dev
# Created postgresql-metric-65240 as DATABASE_URL
# pip install psycopg2-binary

import os
import psycopg2


class BotDataBase:
    @staticmethod
    def connect():
        DATABASE_URL = os.environ['postgresql-metric-65240']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        pass
    pass

