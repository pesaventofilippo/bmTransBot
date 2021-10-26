'''BM Translator Telegram Bot'''
from time import sleep
from threading import Thread
from json import load as jsload
from os.path import abspath, dirname, join
from hashlib import sha256
from telepotpro import Bot, glance
from telepotpro.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepotpro.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


BOT = None


def reply_chat_message(msg) -> None:
    '''This function is called when the bot receives a chat message'''
    chat_id = msg['chat']['id']
    if chat_id > 0:
        BOT.sendMessage(
            chat_id,
            "Hi! I'm the BM Translator Bot 👋\n"
            "You can type @bmTransBot on any chat to display a message "
            "with \"bm style\", like <i>ThIs SeNtEnCe</i>!\n\n"
            "Press the button below to try now!",
            parse_mode = "HTML",
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            text = "💬 Try me!",
                            switch_inline_query = "Hello!"
                        )
                    ]
                ]
            )
        )


def reply_inline_query(msg) -> None:
    '''This function is called when the bot receives an inline query'''
    query_id, _, query_string = glance(msg, flavor="inline_query")

    parsed = ""
    upper = True
    for character in query_string:
        if character.isalpha():
            parsed += character.upper() if upper else character.lower()
            upper = not upper
        else:
            parsed += character

    if parsed:
        desc = parsed if len(parsed) < 18 else parsed[:15] + "..."
        sha_id = sha256(parsed.encode("utf-8")).hexdigest()
        sha_bm_id = sha256((parsed+"!11!!1").encode("utf-8")).hexdigest()
        results = [
            InlineQueryResultArticle(
                id = sha_id,
                title = "BM Translate",
                input_message_content = InputTextMessageContent(
                    message_text = parsed
                ),
                description = desc
            ),
            InlineQueryResultArticle(
                id = sha_bm_id,
                title = "BM Translate!11!!1",
                input_message_content = InputTextMessageContent(
                    message_text = parsed + "!11!!1"
                ),
                description = desc + "!11!!1"
            )
        ]
    else:
        results = []
    BOT.answerInlineQuery(
        query_id,
        results,
        cache_time = 86400,
        is_personal = False
    )


# Callback lambda functions
accept_message = lambda msg: Thread(target=reply_chat_message, args=[msg]).start()
incoming_query = lambda msg: Thread(target=reply_inline_query, args=[msg]).start()


def main() -> None:
    '''
    Funzione main del bot telegram, workflow:
        - legge il file di configurazione
        - inizializza il bot
        - ascolta i messaggi
    '''
    global BOT

    with open(
            join(
                dirname(abspath(__file__)),
                "settings.json"
            ),
            "r",
            encoding="UTF-8"
            ) as settings_file:
        js_settings = jsload(settings_file)

    BOT = Bot(js_settings["token"])

    BOT.message_loop(
        callback = {
            'chat': accept_message,
            'inline_query': incoming_query
        }
    )

    print("Bot Started!")
    while True:
        sleep(60)


if __name__ == '__main__':
    main()
