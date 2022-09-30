import telebot
from telebot import types

import psycopg2

from config import telegram_token, telegram_users, database, user, password, host, port
from constants import LogPhrases, CommandDb

bot = telebot.TeleBot(telegram_token)

data_base = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port=port
)
cursor = data_base.cursor()


def get_numbers_orders():
    """The function in which we get the order numbers from the database"""
    cursor.execute(CommandDb.COMMAND_SELECT_NUMBERS_ORDERS)
    numbers_orders = cursor.fetchall()
    numbers_orders_for_sort = []

    for number in numbers_orders:
        numbers_orders_for_sort.append(number[0])

    return numbers_orders_for_sort


def get_status_delivery(number_order):
    """The function in which we get the status from the database"""
    cursor.execute(CommandDb.COMMAND_SELECT_STATUSES_DELIVERY_TIME, (number_order,))
    status_delivery_time = cursor.fetchone()

    return status_delivery_time[0]


@bot.message_handler(commands=['start'])
def start_message(message):
    """Function using handler for message /start in telegram bot"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(LogPhrases.BUTTON_CHECK_TG)
    markup.add(button)
    bot.send_message(message.chat.id, LogPhrases.HELLO_TELEGRAM, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_answer_users(message):
    """A function using handler for the text content type in the telegram bot.
    Here we accept the message from the button and the order number.
    """
    if message.text == LogPhrases.BUTTON_CHECK_TG:
        bot.send_message(message.chat.id, LogPhrases.NUMBER_ORDER_TG)

    elif int(message.text) in get_numbers_orders():
        bot.send_message(message.chat.id,
                         LogPhrases.STATUS_DELIVERY_TG.format(int(message.text),
                                                              get_status_delivery(int(message.text))))


def send_change_delivery_time(number_order, last_date, new_date):
    """A function that sends a message to telegram if the delivery date has been changed.
    Accepts arguments: order number, delivery date passed, new delivery date
    """
    for id_user in telegram_users:
        bot.send_message(id_user, LogPhrases.CHANGE_DELIVERY_TIME_TG.format(number_order, last_date, new_date))
