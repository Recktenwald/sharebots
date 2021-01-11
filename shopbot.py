#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram bot for keeping a shopping list.
"""

import logging
import json 
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class ShoppingDB:
    """Wrapper for abstracting shopping list textfile i/o"""

    def __init__(self, name="shopping_list.csv"):
        """Find or create a textfile to store the shopping list in"""
        if not os.path.isfile(name):
            with open(name, "w") as shopping_list_file:
                shopping_list_file.write('test')

        self.shopping_list_file = name
    
    def read(self, tag=None):
        """Read from storage, filter for tag. 
        Returns list of shopping items."""
        with open(self.shopping_list_file, "r") as f:
            return f.read().splitlines()

    def write(self, string):
        """Write string to storage"""
        with open(self.shopping_list_file, "w") as f:
            f.write(string)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi Bubus!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def parse(update, context):
    """Parse text for commands."""
    shopping_db = ShoppingDB()
    shopping_list = shopping_db.read()

    text = update.message.text.lower()
    lines = text.splitlines()
    if text is None:
        update.message.reply_text('Error. Empty text.')

    elif 'list' in lines[0] or 'ls' in lines[0][0:3]:
        commands = lines[0].split(' ')
        filter_tag = None
        if len(commands) > 1:
            filter_tag = commands[1]
        if len(shopping_list) == 0:
            update.message.reply_text('Shopping list is empty.')
        else:
            reply = ''
            if filter_tag:
                for item in shopping_list:
                    if filter_tag in item:
                        reply += str(item) + '\n'
            else:
                i = 0
                for item in shopping_list:
                    reply += str(i) + '. ' + str(item) + '\n'
                    i += 1
            update.message.reply_text(reply)

    elif 'clear' in lines[0]:
        shopping_list.clear()
        update.message.reply_text(f'List cleared.')

    elif 'rm' in lines[0] or 'remove' in lines[0]:
        # Extract all numbers from all lines
        removal_indices = []
        for line in lines:
            removal_indices += [int(word) for word in line.split() if word.isdigit()]
        # Check if indices occur in shopping list
        checked_indices = [num for num in removal_indices if num >= 0 and num < len(shopping_list)]
        # Remove indicated items from list - start with largest to prevent re-indexing of list
        reply = 'Removed:\n'
        for index in sorted(checked_indices, reverse=True):
            removed_item = shopping_list.pop(index)
            reply += str(removed_item) + '\n'

        update.message.reply_text(reply)

    else:
        shopping_list += lines
        update.message.reply_text(f'Added {len(lines)} items.')


    shopping_db.write('\n'.join(shopping_list))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def read_secrets(path=None, token_name='shopbot_token'):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    absolute_path = os.path.join(__location__, path)

    with open(path, 'r') as infile:
        json_dict = json.load(infile)
    api_token = json_dict[token_name]
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
