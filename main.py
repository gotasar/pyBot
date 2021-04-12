# https://api.telegram.org/bot1671733318:AAGZe8uuEOkQtTwT8McKa9LyV5JhQGTwt5g/setWebhook?url=https://thawing-badlands-72124.herokuapp.com/
# ssh -R 80:localhost:5000 localhost.run

from flask import Flask, request, jsonify

from tb_static import TB
from db_static import DB
from bot_translator import bot_translator

bot = TB.bot()
conn = DB.conn()
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        bot_translator.processing(message)
        return jsonify(message)
    return '<h1> This is end <h1>'


if __name__ == '__main__':
    app.run()

