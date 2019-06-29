#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
import sqlite3

import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

update_id = None
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()


def main():
    """Run the bot."""
    global update_id
    bot = telegram.Bot('887277310:AAGP9uz9SnqM1izXCjrnN1Owfx06n5ZNeko')

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            if update.message.text[0] == '+' or update.message.text[0] == '-':
                update.message.reply_text('хорош, '+str(update.message.text)+' паков')
                into_db(update.effective_message.date, update.message.text, update.effective_chat.id, update.effective_user.name)


def into_db(message_date, message_text, chat_id, user_name):
    print(message_date.isoformat(sep=' '), message_text, chat_id, user_name)
    cursor.execute("""INSERT INTO pack_counter (
                     datetime,
                     message,
                     chat_id,
                     user_name
                    )
                    VALUES
                     ('%s', '%s' ,'%s', '%s');""" % (message_date.isoformat(sep=' '), message_text, chat_id, user_name))

    conn.commit()


if __name__ == '__main__':
    main()
