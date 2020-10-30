from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import re
from gplink_tokens import tokens
from os import environ
import aiohttp



BOT_TOKEN = environ.get('BOT_TOKEN')
def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("📌 Support Group", url='https://t.me/AI_BOT_HELP'),
            InlineKeyboardButton("🔖 Projects Channel", url='https://t.me/AI_bot_projects'),
        ],
        [
            InlineKeyboardButton("🧐 How to use me", url='https://telegra.ph/How-to-use-me-10-29'),
            InlineKeyboardButton("👨 Master", url='https://t.me/pppppgame'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"Hi! Mr {update.message.from_user.first_name}\n\nI'm GPlink bot. Just send me link and get short link\n\n/help for more help\n\nyou have to autherise me to use this bot use /auth\nyour api token is safe with me I will not share it \n\nany doubt ask here 👉 @AI_BOT_HELP\n\n©️ @AI_bot_projects", reply_markup=reply_markup)


def help_command(update, context):

    update.message.reply_text("Hello\n\nFirst you have to get your API TOKEN OF GPLINK by using /auth \n\nafter that copy that link from GPLINK TOOLS API\n\nit will look like this 👉 https://gplinks.in/api?api=6a4cb74d70edd33a&\nsent it to me\n\n👍 now you are done just sent any link to me")

    
def auth(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Autherise me ", url='https://gplinks.in/member/tools/api'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('please login to your gplink account by pressing the button below and copy paste the api url here\n\neg: https://gplinks.in/api?api=6a4cb74d70edd86803333333333a&', reply_markup=reply_markup)
    

def echo(update, context):

    if 'https://gplinks.in/api?api=' in str(update.message.text):
        chat = str(update.message.chat_id)
        url = update.message.text.replace("https://gplinks.in/api?api=", "")
        token = re.sub("&.*", "", url)
        tokens[chat] = str(token)
        with open('gplink_tokens.py', 'w') as file:
            file.write('tokens = ' + str(tokens))
            update.message.reply_text(f'🎉 congratulations \n\nYour 😇 CHAT_ID : {chat} IS REGISTERED WITH GPLINK API TOKEN : {token}\n\nIf you sent me a different API URL I will reassign your GPLINK API TOKEN')
    elif 'https://gplinks.in/api?api=' not in str(update.message.text) and (re.search('^http://.*', str(update.message.text)) or re.search('^https://.*', str(update.message.text))):
        try:
            chat = str(update.message.chat_id)
            gptoken = tokens[chat]
            url_convert = update.message.text
        except:
            update.message.reply_text("Your api token is missing please autherise me by /auth for using me 🤪")

        req = requests.get(f'https://gplinks.in/api?api={gptoken}&url={url_convert}')
        r = json.loads(req.content)

        if r['status'] == 'success':
            update.message.reply_text(' Status : ' + r['status'])
            update.message.reply_text(' shortenedUrl : ' + r['shortenedUrl'])
        if r['status'] == 'error':
            update.message.reply_text(' Error : ' + r['message'])


def main():
    updater = Updater(
        BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("auth", auth))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
