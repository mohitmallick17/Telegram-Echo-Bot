import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

load_dotenv('config.env')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello. I am a bot ')


def echo(update, context):
    msg = update.message
    auth_chat = os.getenv('AUTHORIZED_CHATS')[1:-1].split(',')
    if msg.video and msg.video != {}:
        for chat in auth_chat:
            context.bot.send_video(chat_id=chat, video=update.message.video, caption=msg.caption)
    elif msg.document and msg.document != {}:
        for chat in auth_chat:
            context.bot.send_document(chat_id=chat, document=update.message.document, caption=msg.caption)
    elif msg.text:
        for chat in auth_chat:
            if 'mega' in chat or 't.me' in chat:
                context.bot.send_message(chat_id=chat, text=update.message.text)
    elif msg.video_note:
        for chat in auth_chat:
            context.bot.send_video_note(chat_id=chat, video_note=update.message.video_note)
    elif msg.photo and msg.photo != []:
        for chat in auth_chat:
            context.bot.send_photo(chat_id=chat, photo=msg.photo[0]['file_id'])


cmd = CommandHandler('start', start)
echo_handle = MessageHandler(Filters.all & (~Filters.command), echo)
dispatcher.add_handler(cmd)
dispatcher.add_handler(echo_handle)
updater.start_polling()
