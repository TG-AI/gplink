# import pyshorteners
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
import requests
import json
import re
from gplink_tokens import tokensp
from golink_tokens import tokensg
from os import environ
import aiohttp

BOT_TOKEN = environ.get('BOT_TOKEN')
def start(update: Update, context: CallbackContext):
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


    
    
def help_command(update: Update, context: CallbackContext):

    update.message.reply_text('Hello\n\nFirst you have to get your API TOKEN OF GPLINK by using /auth \n\nafter that copy that link from GPLINK TOOLS API\n\nit will look like this 👉 https://gplinks.in/api?api=6a4cb74d70edd33a&\nsent it to me\n\n👍 now you are done just sent any link to me')
    
def auth(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Autherise me ", url='https://gplinks.in/member/tools/api'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('please login to your gplink account by pressing the button below and copy paste the api url here\n\neg: https://gplinks.in/api?api=6a4cb74d70edd86803333333333a&', reply_markup=reply_markup)

    
def ech(update: Update, context: CallbackContext):
    if 'https://golinksrt.xyz/api?api=' in str(update.message.text):
        chat = str(update.message.chat_id)
        url = update.message.text.replace("https://golinksrt.xyz/api?api=", "")
        tokeno = re.sub("&.*", "", url)
        tokensg[chat] = str(tokeno)
        with open('golink_tokens.py', 'w') as file:
            file.write('tokensg = ' + str(tokensg))
            update.message.reply_text(f'🎉 congratulations \n\nYour 😇 CHAT_ID : {chat} IS REGISTERED WITH GOLINK API TOKEN : {tokeno}\n\nIf you sent me a different API URL I will reassign your GOLINK API TOKEN')
 
def echo(update: Update, context: CallbackContext):
    if 'https://gplinks.in/api?api=' in str(update.message.text):
        chat = str(update.message.chat_id)
        url = update.message.text.replace("https://gplinks.in/api?api=", "")
        tokenp = re.sub("&.*", "", url)
        tokensp[chat] = str(tokenp)
        with open('gplink_tokens.py', 'w') as file:
            file.write('tokensp = ' + str(tokensp))
            update.message.reply_text(f'🎉 congratulations \n\nYour 😇 CHAT_ID : {chat} IS REGISTERED WITH GPLINK API TOKEN : {tokenp}\n\nIf you sent me a different API URL I will reassign your GPLINK API TOKEN')
 
def ecv(update: Update, callback_query):
    if 'https://golinksrt.xyz/api?api=' not in str(update.message.text) and 'https://gplinks.in/api?api=' not in str(update.message.text) and (re.search('^http://.*', str(update.message.text)) or re.search('^https://.*', str(update.message.text))):  
         keyboard = [
                 [
                     InlineKeyboardButton("gp link", callback_data="gplink"),
                     InlineKeyboardButton("go link", callback_data="golink"),
                 ],
             ]

         reply_markup = InlineKeyboardMarkup(keyboard)

         update.message.reply_text('plea', reply_markup=reply_markup)

def golink(update: Update, callback_query):  
    if callback_query.data == "golink":
       try:
            chat = str(update.message.chat_id)
            gotoken = tokensg[chat]
            url_convert = update.message.text
       except:
            callback_query.message.reply_text("Your api token is missing please autherise me by /auth for using me 🤪")

       req = requests.get(f'https://golinksrt.xyz/api?api={gotoken}&url={url_convert}')
       r = json.loads(req.content)

       if r['status'] == 'success 👍':
           callback_query.message.reply_text(' Status : ' + r['status'])
           callback_query.message.reply_text(' shortenedUrl : ' + r['shortenedUrl'])
       if r['status'] == 'Sorry something went wrong pleas try again 🙏':
           callback_query.message.reply_text(' Error : ' + r['message'])          
 

def gplink(update: Update, callback_query): 
    if callback_query.data == "gplink":
       try:
            chat = str(update.message.chat_id)
            gptoken = tokensp[chat]
            url_convert = update.message.text
       except:
           callback_query.message.reply_text("Your api token is missing please autherise me by /auth for using me 🤪")

       req = requests.get(f'https://gplinks.in/api?api={gptoken}&url={url_convert}')
       r = json.loads(req.content)

       if r['status'] == 'success 👍':
           callback_query.message.reply_text(' Status : ' + r['status'])
           callback_query.message.reply_text(' shortenedUrl : ' + r['shortenedUrl'])
       if r['status'] == 'Sorry something went wrong pleas try again 🙏':
           callback_query.message.reply_text(' Error : ' + r['message'])                       
            
def main():
    updater = Updater(
        BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("auth", auth))
    dp.add_handler(CommandHandler("goapi", ech))
    dp.add_handler(CommandHandler("gpapi", echo))
    dp.add_handler(CallbackQueryHandler("gplink", gplink))
    dp.add_handler(CallbackQueryHandler("golink", golink))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ecv))
    updater.start_polling()  
    updater.idle() 


if __name__ == '__main__':
    main()
