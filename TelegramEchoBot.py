import logging
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
####
# Author MohitMallick17@github
# Disclaimer :
# I am not responsible if your bot is u
#
#
####
load_dotenv('config.env')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello. I am a bot ')


def echo(update, context):
    msg = update.message
    if msg.video and msg.video != {}:
        context.bot.send_video(chat_id=update.effective_chat.id, video=update.message.video, caption=msg.caption)
    if msg.sticker and msg.sticker != {}:
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=update.message.sticker)
    elif msg.document and msg.document != {}:
        context.bot.send_document(chat_id=update.effective_chat.id, document=update.message.document, caption=msg.caption)
    elif msg.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    elif msg.game:
        context.bot.send_game(chat_id=update.effective_chat.id, game=update.message.game)
    elif msg.audio:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=update.message.audio)
    elif msg.voice:
        context.bot.send_voice(chat_id=update.effective_chat.id, voice=update.message.voice)
    elif msg.video_note:
        context.bot.send_video_note(chat_id=update.effective_chat.id, video_note=update.message.video_note)
    elif msg.contact:
        context.bot.send_contact(chat_id=update.effective_chat.id, contact=update.message.contact, caption=msg.caption)
    elif msg.location:
        context.bot.send_location(chat_id=update.effective_chat.id, location=update.message.location, caption=msg.caption)
    elif msg.venue:
        context.bot.send_venue(chat_id=update.effective_chat.id, venue=update.message.venue, caption=msg['caption'])
    elif msg.photo and msg.photo != []:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=msg.photo[0]['file_id'])


cmd = CommandHandler('start', start)
echo_handle = MessageHandler(Filters.all & (~Filters.command), echo)
dispatcher.add_handler(cmd)
dispatcher.add_handler(echo_handle)
updater.start_polling()
