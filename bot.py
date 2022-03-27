
import logging
import requests
import json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

text = ""
phones = []
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('/start, /help, /messages, /create, /phones, /send')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/start, /help, /messages, /create, /phones, /send')


def echo(update, context):
    try:
        message = json.loads(update.message.text)
        req = requests.post("http://127.0.0.1:8000/whatsapp/createmessage/", data=message)
        update.message.reply_text(req.status_code)
    except:
        message = update.message.text.split("-")
        for msg in message:
            req = requests.post("http://127.0.0.1:8000/whatsapp/phones/", data={"phone":msg})
        update.message.reply_text(req.status_code)

            



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def messages(update, context):
    req = requests.get("http://127.0.0.1:8000/whatsapp/createmessage/")
    response = json.loads(req.content)
    for message in response:
        update.message.reply_text(f'ID {message["id"]}\nTEXT\n{message["text"]}')
        phones = ""
        for phone in message["phones_obj"]:
            phones += f'\n{str(phone["id"])} : {str(phone["phone"])}'
        update.message.reply_text(phones)

def phones(update, context):
    req = requests.get("http://127.0.0.1:8000/whatsapp/phones/")
    response = json.loads(req.content)
    for phone in response:
        update.message.reply_text(f"{str(phone['id'])}: {str(phone['phone'])}") 

def createmessage(update, context):
    update.message.reply_text("""{\n"text": "",\n"user": 1,\n"phones": []\n}""")

def send(update, context):
    requests.post(f"http://127.0.0.1:8000/whatsapp/sendmessage/{context.args[0]}/")
    update.message.reply_text("Done!") 



def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5141656941:AAGLVKX656U5Ls2XgkML9BS30q7KvLBg2K4", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("messages", messages))
    dp.add_handler(CommandHandler("create", createmessage))
    dp.add_handler(CommandHandler("phones", phones))
    dp.add_handler(CommandHandler("send", send))



    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    updater.idle()


if __name__ == '__main__':
    main()
