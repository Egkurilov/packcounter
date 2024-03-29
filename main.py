#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sqlite3

import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import sys
import time

import config


reload(sys)
sys.setdefaultencoding('utf-8')

update_id = None
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

RULE = '''Привет, игра началась!
            Правила - простые, каждый раз когда ты сдал или отвез паки, пиши в чат + и количество паков.
            Побеждает тот, кто занял первое место по итогу дня. (счетчик обновляется каждую ночь). 
            Доступные на данный момент команды:
            /score
            /info'''


def main():
    """Run the bot."""
    global update_id
    bot = telegram.Bot(config.TOKEN)

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


def info(update):
    update.message.reply_text('Hi!')


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:  # your bot can receive updates without messages
            if update.message.text is not None:
                if update.message.text == '/score@packscoreBot':
                    bot.send_message(update.effective_chat.id, repr(select_db_info()).decode("unicode_escape"))
                if update.message.text == '/info@packscoreBot':
                    update.message.reply_text("Правила следующие:")
                    bot.send_message(update.effective_chat.id, RULE)
                if update.message.text[0] == '+':
                    if update.message.text[1:].isnumeric():
                        update.message.reply_text(str(update.message.text)+' паков')
                        into_db(update.effective_message.date, update.message.text, \
                                update.effective_chat.id, update.effective_user.name)
                    else:
                        update.message.reply_text("Try Again")
                else:
                        pass


def into_db(message_date, message_text, chat_id, user_name):
    cursor.execute("""INSERT INTO pack_counter (
                     datetime,
                     message,
                     chat_id,
                     user_name
                    )
                    VALUES
                     ('%s', '%s' ,'%s', '%s');""" %
                   (message_date.isoformat(sep=' '), message_text, chat_id, user_name))

    conn.commit()


def select_db_info():
    cursor.execute("""SELECT distinct(user_name), sum(message) FROM pack_counter
                              WHERE user_name is not null
                              AND date(datetime) = date('now') 
                              GROUP BY user_name
                              ORDER BY message ASC""")
    result = cursor.fetchall()
    gg= " ".join(str(x) for x in result)
    return(gg)




if __name__ == '__main__':
    main()
