#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram bot for keeping a shopping list.
"""

import logging
import json 

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


#shopping_list = ['start_item', 'next_item']
shopping_list = [] 


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi Bubus!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def parse(update, context):
    """Parse text for commands."""
    global shopping_list

    text = update.message.text.lower()
    if text is None:
        update.message.reply_text('Error. Unknown Error.')

    elif 'list' in text or text == 'ls':
        if len(shopping_list) == 0:
            update.message.reply_text('Shopping list is empty.')
        else:
            reply = '\n'.join(shopping_list)
            update.message.reply_text(reply)

    elif '+' in text:
        item = text.split('+')[1].strip()
        shopping_list += [item]
        update.message.reply_text(f'Added "{item}"')

    elif 'add' in text:
        item = text.split('add')[1].strip()
        shopping_list += [item]
        update.message.reply_text(f'Added "{item}"')

    elif '-' in text:
        item = text.split('-')[1].strip()
        if item in shopping_list:
            shopping_list.remove(item)
            update.message.reply_text(f'Removed "{item}"')
        else:
            update.message.reply_text(f'"{item}" not found.')

    elif 'remove' in text or 'rm' in text:
        item = text.split(' ')[1].strip()
        if item in shopping_list:
            shopping_list.remove(item)
            update.message.reply_text(f'Removed "{item}"')
        else:
            update.message.reply_text(f'"{item}" not found.')

    elif 'clear' in text:
        shopping_list.clear()
        update.message.reply_text(f'List cleared.')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def read_secrets(path=None):

    with open(path, 'r') as infile:
        json_dict = json.load(infile)
    api_token = json_dict['token']
    return api_token

def main():
    """Start the bot."""
    token = read_secrets(path='./secrets.json')

    # Create the Updater and pass it your bot's token.
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, parse))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
