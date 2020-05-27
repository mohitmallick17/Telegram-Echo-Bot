import logging

import telegram
from dotenv import load_dotenv
from telegram.utils.request import Request
from telegram.ext import Updater, MessageHandler, Filters, messagequeue as mq, CommandHandler
import os


####
# Author MohitMallick17@github
# Disclaimer :
# I am not responsible if your bot is used by people with wrong intentions which may lead to a permanent ban
# You are free to modify the source code as per need.
# Plagiarism shall never be entertained, of course
####

class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''

    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)

    @mq.queuedmessage
    def send_video(self, *args, **kwargs):
        return super(MQBot, self).send_video(*args, **kwargs)

    @mq.queuedmessage
    def send_document(self, *args, **kwargs):
        return super(MQBot, self).send_document(*args, **kwargs)

    @mq.queuedmessage
    def send_photo(self, *args, **kwargs):
        return super(MQBot, self).send_photo(*args, **kwargs)

    @mq.queuedmessage
    def send_video_note(self, *args, **kwargs):
        return super(MQBot, self).send_video_note(*args, **kwargs)

    @mq.queuedmessage
    def send_sticker(self, *args, **kwargs):
        return super(MQBot, self).send_sticker(*args, **kwargs)

    @mq.queuedmessage
    def send_game(self, *args, **kwargs):
        return super(MQBot, self).send_game(*args, **kwargs)

    @mq.queuedmessage
    def send_audio(self, *args, **kwargs):
        return super(MQBot, self).send_audio(*args, **kwargs)

    @mq.queuedmessage
    def send_video_note(self, *args, **kwargs):
        return super(MQBot, self).send_video_note(*args, **kwargs)

    @mq.queuedmessage
    def send_voice(self, *args, **kwargs):
        return super(MQBot, self).send_voice(*args, **kwargs)

    @mq.queuedmessage
    def send_contact(self, *args, **kwargs):
        return super(MQBot, self).send_contact(*args, **kwargs)

    @mq.queuedmessage
    def send_location(self, *args, **kwargs):
        return super(MQBot, self).send_location(*args, **kwargs)

    @mq.queuedmessage
    def send_venue(self, *args, **kwargs):
        return super(MQBot, self).send_venue(*args, **kwargs)

    @mq.queuedmessage
    def send_location(self, *args, **kwargs):
        return super(MQBot, self).send_location(*args, **kwargs)


load_dotenv('config.env')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
request = Request(con_pool_size=8)
q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
auth_chats=os.getenv('AUTHORIZED_CHATS')[1:-1].replace(' ','').split(',')

class NoTokenFoundError(Exception):
    pass


token = os.getenv('BOT_TOKEN')
if token is None or token == '':
    raise NoTokenFoundError("Error. Your Token String in config.env is empty. Please fill your token and re-run the "
                            "script.")
mybot = MQBot(token, request=request, mqueue=q)
updater = Updater(bot=mybot, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello. I am a bot.')


def echo(update, context):
    if 'ALL' in auth_chats or str(update.effective_chat.id) in auth_chats:
        msg = update.message
        if msg.video and msg.video != {}:
            mybot.send_video(chat_id=update.effective_chat.id, video=update.message.video, caption=msg.caption)
        if msg.sticker and msg.sticker != {}:
            mybot.send_sticker(chat_id=update.effective_chat.id, sticker=update.message.sticker)
        elif msg.document and msg.document != {}:
            mybot.send_document(chat_id=update.effective_chat.id, document=update.message.document, caption=msg.caption)
        elif msg.text:
            mybot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        elif msg.game:
            mybot.send_game(chat_id=update.effective_chat.id, game=update.message.game)
        elif msg.audio:
            mybot.send_audio(chat_id=update.effective_chat.id, audio=update.message.audio)
        elif msg.voice:
            mybot.send_voice(chat_id=update.effective_chat.id, voice=update.message.voice)
        elif msg.video_note:
            mybot.send_video_note(chat_id=update.effective_chat.id, video_note=update.message.video_note)
        elif msg.contact:
            mybot.send_contact(chat_id=update.effective_chat.id, contact=update.message.contact, caption=msg.caption)
        elif msg.location:
            mybot.send_location(chat_id=update.effective_chat.id, location=update.message.location, caption=msg.caption)
        elif msg.venue:
            mybot.send_venue(chat_id=update.effective_chat.id, venue=update.message.venue, caption=msg['caption'])
        elif msg.photo and msg.photo != []:
            mybot.send_photo(chat_id=update.effective_chat.id, photo=msg.photo[0]['file_id'])


cmd = CommandHandler('start', start)
echo_handle = MessageHandler(Filters.all & (~Filters.command), echo)
dispatcher.add_handler(cmd)
dispatcher.add_handler(echo_handle)
updater.start_polling()
