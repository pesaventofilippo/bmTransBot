from time import sleep
from telepotpro import Bot, glance
from telepotpro.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepotpro.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from json import load as jsload
from os.path import abspath, dirname, join

with open(join(dirname(abspath(__file__)), "settings.json")) as settings_file:
    js_settings = jsload(settings_file)

bot = Bot(js_settings["token"])


def reply(msg):
    chatId = msg['chat']['id']

    if chatId > 0:
        bot.sendMessage(chatId, "Hi! I'm the BM Translator Bot 👋\n"
                                "You can type @bmTransBot on any chat to display a message "
                                "with \"bm style\", like <i>ThIs SeNtEnCe</i>!\n\n"
                                "Press the button below to try now!", parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                        InlineKeyboardButton(text="💬 Try me!", switch_inline_query="Hello!")
                                    ]])
                        )


def query(msg):
    queryId, chatId, queryString = glance(msg, flavor="inline_query")

    parsed = ""
    upper = True
    for c in queryString:
        if c.isalpha():
            parsed += c.upper() if upper else c.lower()
            upper = not upper
        else:
            parsed += c

    if parsed:
        desc = parsed if len(parsed) < 18 else parsed[:15] + "..."
        results = [
            InlineQueryResultArticle(
                id=f"#{queryString}",
                title="BM Translate",
                input_message_content=InputTextMessageContent(
                    message_text=parsed
                ),
                description=desc
            ),
            InlineQueryResultArticle(
                id=f"#{queryString}_1!",
                title="BM Translate!11!!1",
                input_message_content=InputTextMessageContent(
                    message_text=parsed + "!11!!1"
                ),
                description=desc + "!11!!1"
            )
        ]
    else:
        results = []
    bot.answerInlineQuery(queryId, results, cache_time=86400, is_personal=False)


def accept_message(msg):
    Thread(target=reply, args=[msg]).start()

def incoming_query(msg):
    Thread(target=query, args=[msg]).start()

bot.message_loop(
    callback={'chat': accept_message, 'inline_query': incoming_query}
)

while True:
    sleep(60)
