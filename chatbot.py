import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

global redis1
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['TELEGRAM']['ACCESS_TOKEN']
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']),
                        password=(config['REDIS']['PASSWORD']),
                        port=(config['REDIS']['REDISPORT']),
                        decode_responses=(config['REDIS']['DECODE_RESPONSES']),
                        username=(config['REDIS']['USER_NAME']))

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equip_chatgpt)

    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('get', get))
    dispatcher.add_handler(CommandHandler('delete', delete))
    dispatcher.add_handler(chatgpt_handler)

    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update, context: CallbackContext) -> None:
    update.message.reply_text("Helping you helping you.")

def add(update, context: CallbackContext) -> None:
    try:
        global redis1
        logging.info(context.args)
        msg = context.args[0]
        redis1.incr(msg)

        update.message.reply_text("You have said " + msg + " for " + redis1.get(msg) + " times.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /add <keyword>")

def get(update, context: CallbackContext) -> None:
    try:
        global redis1
        logging.info(context.args)
        msg = context.args[0]
        times = redis1.get(msg) if redis1.get(msg) else 0
        update.message.reply_text("You have said " + msg + " for " + str(times) + " times.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /get <keyword>")

def delete(update, context: CallbackContext) -> None:
    try:
        global redis1
        logging.info(context.args)
        msg = context.args[0]
        redis1.delete(msg)
        update.message.reply_text("You have deleted the keyword " + msg)
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /delete <keyword>")

def equip_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__ == '__main__':
    main()