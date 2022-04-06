
import logging
from os import access
import re
import requests
import json


from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import CallbackContext, CommandHandler, Updater , Filters , MessageHandler

global message

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
url = 'http://127.0.0.1:8000'
text = ""
phones = []
header_access_token = {}
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    req = requests.post(url+"/auth/login/", data={"telegram_id":update.message.chat_id})
    keys = ReplyKeyboardMarkup([['/start'], ['/help'], ['/messages'], ['/create'], ['/phones'], ])
    update.message.reply_text("به ربات کنترل واتسآپ Nova خوش آمدید.", reply_markup=keys)
    if req.status_code==500:
        update.message.reply_text("شما دسترسی لازم برای استفاده از ربات را ندارید لطفا به آیدی پشتیبانی پیام دهید.")
        return None
    else:
        global header_access_token
        response = json.loads(req.content)
        access_token = response.get('access')
        header_access_token = {f"Authorization":"Bearer {access_token}"}

def help(update, context):
    """Send a message when the command /help is issued."""
    keys = ReplyKeyboardMarkup([['/start'], ['/help'], ['/messages'], ['/create'], ['/phones'], ])
    update.message.reply_text('برای ایجاد پیام از دستور /create\nبرای دیدن پیام های موجود از دستور /messages\nبرای دیدن شماره تلفن های ثبت شده از دستور /phones\nبرای ارسال پیام از دستور /send \n استفاده کنید', reply_markup=keys)


def echo(update, context):
    message = update.message.text.split("-")
    for msg in message:
        req = requests.post(url+"/whatsapp/phones/", data={"phone":msg})
    update.message.reply_text(req.status_code)


    

def message_text(update, context):
    global message
    if len(message) > 0 :
        if message.get("phones") is not None :
            
            if update.message.text == "Send":
                message.update({"user":1})
                req = requests.post(url+f"/whatsapp/sendmessage/", message)
                if req.status_code == 201:
                    keys = ReplyKeyboardMarkup([['/start'], ['/help'], ['/messages'], ])
                    update.message.reply_text("ثبت شد", reply_markup=keys)

                    message = {}
                else:
                    update.message.reply_text("خطا")
        else:
            phones = update.message.text.split('-')
            result = "شماره های زیر اضافه شدند:"
            req = requests.get(url+"/whatsapp/phones/")
            try:
                response = json.loads(req.content)
            except:
                response = [{'phone':'+989120000000'}]
            exist_phones = []
            message_phones = []
            for resp in response:
                exist_phones.append(resp["phone"])
            for phone in phones:
                if re.compile('^989[0-9]{9,9}$').match(phone):
                    valid_phone = "+"+phone
                    if not valid_phone in exist_phones:
                        requests.post(url+"/whatsapp/phones/", data={"phone":valid_phone})
                    message_phones.append(valid_phone)
                    result+=f"\n{valid_phone}"
                else:
                    update.message.reply_text(f"شماره وارد شده {phone} نامعتبر است.")
            if len(message_phones) > 0:
                req = requests.get(url+"/whatsapp/phones/")
                try:
                    response = json.loads(req.content)
                except:
                    response = [{'phone':'+989120000000'}]
                message_phone_id = []
                for resp in response:
                    if resp["phone"] in message_phones:
                        message_phone_id.append(resp["id"])
                message.update({"phones":message_phone_id})
            key = ReplyKeyboardMarkup([["Send"]])
            update.message.reply_text(result, reply_markup=key)
    else:
        message.update({"text":update.message.text})
        update.message.reply_text("لطفا شماره های مورد نظر را به صورت 989100000000 وارد کنید(اگر تعداد شماره ها بیشتر از 1 است با - از هم جدا کنید)")
    



def createmessage(update, context):
    global message

    update.message.reply_text("لطفا متن پیام را وارد کنید")
    message = {}
    dp.add_handler(MessageHandler(Filters.text , message_text))




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def messages(update, context):
    global header_access_token
    req = requests.get(url+"/whatsapp/createmessage/", headers=header_access_token)
    try:
        response = json.loads(req.content)
    except:
        update.message.reply_text("پیامی برای نمایش وجود ندارد")
        return None
    for message in response:
        phone_str = ""
        for ph in message["phones_obj"]:
            phone_str += " - "+ph["phone"]
        update.message.reply_text(f'آیدی:"{message["id"]}"\nمتن:"{message["text"][:30]}"\nشماره ها:"{phone_str}"')

def phones(update, context):
    req = requests.get(url+"/whatsapp/phones/")
    response = json.loads(req.content)
    for phone in response:
        update.message.reply_text(f"{str(phone['id'])}: {str(phone['phone'])}") 





def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5154862736:AAFEjZIbLSt6Y7ZxzOdKBUKSwwPtfOU_SAE", use_context=True)

    # Get the dispatcher to register handlers
    global dp
    dp = updater.dispatcher
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("messages", messages))
    dp.add_handler(CommandHandler("create", createmessage))
    dp.add_handler(CommandHandler("phones", phones))



    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    updater.idle()


if __name__ == '__main__':
    main()
