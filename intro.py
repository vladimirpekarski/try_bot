# -*- coding: utf-8 -*-

import logging

from constants import TOKEN

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (CommandHandler, MessageHandler, Updater,
                          Filters, InlineQueryHandler)
from jenkins_work import get_last_job_status


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I am bot, please talk to me")


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


def last_job_status(bot, update):
    job_id, status = get_last_job_status()
    text = 'Last build id: {}. Status'.format(job_id, status)
    bot.send_message(chat_id=update.message.chat_id, text=text)


def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=
    'Sorry, I didnt understand that command')


start_handler = CommandHandler('start', start)
job_status_handler = CommandHandler('job_status', last_job_status)
caps_handler = CommandHandler('caps', caps, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(job_status_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()