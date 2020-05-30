#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram bot for keeping a shopping list.
"""

import logging
import json 
import os
import pandas as pd

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from uuid import uuid4

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class wg():
    def __init__(self, tasks=['floor', 'kitchen', 'bathroom', 'garbage', 'free'], 
                 members=['lu', 'sophia', 'ms_bubu', 'mr_bubu', 'toni', 'test']):
        self.schedule = pandas.DataFrame(members, columns=tasks)

    def add_member(self, name):
        pass

    def rm_member(self, name):
        pass


    def show_schedule(self):
        print(self.schedule)

    def __str__(self):
        string = 'Members: '
        print(string)


def signup(update, context):
    """Usage: /put value"""
    # Generate ID and seperate value from command
    key = str(uuid4())
    value = update.message.text.partition(' ')[2]

    # Store value
    context.bot_data[key] = value
    
    try:
        username = update.message.chat.username
        update.message.reply_text(username)
    except:
        error_text = f'No username in object: \n{str(update)}'
        update.message.reply_text(error_text)


def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = update.message.text.partition(' ')[2]

    # Load value
    try:
        value = context.bot_data[key]
        update.message.reply_text(value)

    except KeyError:
        update.message.reply_text('Not found')


def show(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('')


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('...')


def help(update, context):
    """Send a message when the command /help is issued."""
    text='Do you want me to sit in a corner and rust, or just fall apart where I’m standing?'
    update.message.reply_text(text)


def lullaby(update, context):
    text="""
    Now the world has gone to bed
    Darkness won't engulf my head
    I can see by infra-red
    How I hate the night
    Now I lay me down to sleep
    Try to count electric sheep
    Sweet dream wishes you can keep
    How I hate the night"""
    update.message.reply_text(text)


def parse(update, context):
    """Parse text for commands."""

    text = update.message.text.lower()


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
    # Read API key from rest
    token = read_secrets(path='./secrets.json', token_name='cleanbot_token')

    # Define updater
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Register commands/handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("lullaby", lullaby))
    dp.add_handler(CommandHandler('signup', signup))
    dp.add_handler(CommandHandler('get', get))
    dp.add_handler(MessageHandler(Filters.text, parse))
    dp.add_error_handler(error)

    # Start
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
