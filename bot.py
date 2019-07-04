import telegram
from telegram.ext import Updater, Dispatcher, MessageHandler, MessageQueue, CommandHandler, Filters

TOKEN = "REDACTED"
bot = telegram.Bot(TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
jq = updater.job_queue
list_of_active_users = dict()
FAIL_TEXT = "متاسفانه مشکلی پیش اومد، لطفا دوباره پیام‌تون رو ارسال کنید."
WELCOME_TEXT = "سلام. به بات پرسش و پاسخ خوش آمدید."
WAIT_TEXT = "پیام شما دریافت شد؛ لطفا شکیبا باشید تا مسئولین جواب بدند."
RESPONDED_TEXT = "جوابتون رو اینجا دادیم"
# must not start with an @
RESPONDER_ID = "REDACTED"
# must start with an @
CHANNEL_ID = "REDACTED"
DEV_ID = "REDACTED"
ASKED_TEXT = "پرسیده اند که"
ANSWERED_TEXT = "و جواب این است که"
HIDDEN_STATE = "مخفی"
SHOWING_STATE = "نمایان"
YOUR_STATE = "وضعیت فعلی شما: "

def start(bot, update):
    message = update.message
    chat_id = message.chat_id
    user = message.from_user.username
    add_to_users(user, chat_id)
    bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)

def receive(bot, update):
    user = username = update.message.from_user
    username = user.username
    message = update.message
    add_to_users(username, message.chat_id)
    if username == RESPONDER_ID:
        receive_from_ta(bot, update)
    else:
        receive_from_users(bot, update, user, message)

def add_to_users(user, chat_id):
    if user not in list_of_active_users.keys():
        list_of_active_users.update({user: {'id': chat_id, 'visible': True}})

def format_tas_outgoing_string(text, answer_text, caption=None):
    half = txt = ""
    checkText = text
    if not text:
        text = caption
    splitMessage = text.split('\n')
    asker = {"name": splitMessage[0], "handle": splitMessage[1][1:]}
    for i in range(2, len(splitMessage)):
        half += str(splitMessage[i])
    if checkText and caption:
        half += "\n" + caption
    if list_of_active_users[asker["handle"]]["visible"]:
        txt = asker["name"]
    txt += "  " + ASKED_TEXT + ":\n" + half + "\n\n" + ANSWERED_TEXT + ":\n" + answer_text
    return txt, asker


def receive_from_ta(bot, update):
    sent_in_channel = None
    answer = update.message
    message = answer.reply_to_message
    caption = message.caption
    answer_text = answer.text
    txt, asker = format_tas_outgoing_string(message.text, answer_text, caption)
    sent_in_channel = returnSentMedia(bot, CHANNEL_ID, message, txt)
    sent_link = sent_in_channel.link
    bot.send_message(chat_id=list_of_active_users[asker["handle"]]["id"],
                     text='<a href="' + sent_link + '">' + RESPONDED_TEXT + '</a>',
                     parse_mode=telegram.ParseMode.HTML)


def not_sent_error(bot, message, ex):
    bot.send_message(chat_id=message.chat_id, text=FAIL_TEXT)
    bot.send_message(chat_id=list_of_active_users[DEV_ID]["id"], text=str(ex) +"\n" + message.chat_id)


def receive_from_users(bot, update, user, message):
    try:
        if is_a_registered_member(user):
            txt = user.full_name + "\n" + "@" + user.username + "\n" + message.text
            bot.send_message(chat_id=list_of_active_users[RESPONDER_ID]["id"], text=txt)
            bot.send_message(chat_id=message.chat_id, text=WAIT_TEXT)
    except Exception as ex:
        not_sent_error(bot, message, ex)


def returnSentMedia(bot, ta_id, message, txt):
    sent_in_channel = None
    if message.video:
        sent_in_channel = bot.send_video(chat_id=ta_id , video=message.video.file_id, caption=txt)
    if message.photo:
        photos = message.photo
        lastPhoto = len(photos) - 1
        sent_in_channel = bot.send_photo(chat_id=ta_id, photo=message.photo[lastPhoto].file_id, caption=txt)
    if message.audio:
        sent_in_channel = bot.send_audio(chat_id=ta_id, photo=message.audio.file_id, caption=txt)
    if message.document:
        sent_in_channel = bot.send_document(chat_id=ta_id, photo=message.document.file_id, caption=txt)
    if not sent_in_channel:
        sent_in_channel = bot.send_message(chat_id=ta_id, text=txt)
    return sent_in_channel


def forward_media(bot, update):
    ta_id = chat_id = list_of_active_users[RESPONDER_ID]["id"]
    message = update.message
    user = message.from_user
    username = user.username
    chat_id = message.chat_id
    add_to_users(username, chat_id)
    txt = ""
    if username != RESPONDER_ID:
        try:
            if message.caption:
                txt += message.caption
            if message.text and txt != "":
                txt += "\n" + message.text
            txt = user.full_name + "\n" + "@" + username + "\n" + txt
            returnSentMedia(bot, ta_id, message, txt)
            bot.send_message(chat_id=message.chat_id, text=WAIT_TEXT)
        except Exception as ex:
            not_sent_error(bot, message, ex)


def is_a_registered_member(user):
    '''
    Will be changed if in a future event we only want the opinion of the participants,
    As of April 3rd, 2019 it's being used for an "Asrane" event, so there's no use to it.
    '''
    return True

def toggle_name_visibility(bot, update):
    message = update.message
    user = message.from_user
    username = user.username
    chat_id = message.chat_id
   
    if username in list_of_active_users.keys():
        user_in_list = list_of_active_users[username]
        user_in_list["visible"] = not user_in_list["visible"] 
        if user_in_list["visible"]:
            bot.send_message(chat_id=chat_id, text=YOUR_STATE + SHOWING_STATE)
        else:
            bot.send_message(chat_id=chat_id, text=YOUR_STATE + HIDDEN_STATE)
        


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('toggle', toggle_name_visibility))
dispatcher.add_handler(MessageHandler(Filters.text, receive))
dispatcher.add_handler(MessageHandler(Filters.audio | Filters.video | Filters.photo | Filters.document, forward_media))


updater.start_polling()