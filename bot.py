import config
from telebot import TeleBot, types, logger
from flask import Flask, request, abort
from time import sleep
import logging

log = logger
logger.setLevel(logging.INFO)

bot = TeleBot(config.API_TOKEN)
app = Flask('webhook')


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(config.WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "I am dumbass. I can do nothing.")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, "Sorry, I'm dumbass. Can't do anything.")


bot.remove_webhook()
sleep(0.1)
bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH)

app.run(host=config.WEBHOOK_LISTEN, port=config.WEBHOOK_LISTEN_PORT)
