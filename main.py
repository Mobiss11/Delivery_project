import time

from datetime import datetime
from threading import Thread

import requests

from telegram import bot
from database import DataBase
from config import sheet_with_data
from constants import LogPhrases


def get_columns_google_table():
    """
    We get the lists from the columns of the Google table
    and converts them into a tuple through the for loop.
    """
    numbers_row = sheet_with_data.col_values(1)
    numbers_order = sheet_with_data.col_values(2)
    cost_in_dollars = sheet_with_data.col_values(3)
    delivery_time = sheet_with_data.col_values(4)
    statuses_delivery = sheet_with_data.col_values(5)

    numbers_row.pop(0)
    numbers_order.pop(0)
    cost_in_dollars.pop(0)
    delivery_time.pop(0)
    statuses_delivery.pop(0)

    datas_for_db = []

    for number, numbers_order, cost_in_dollars, delivery_time, status_delivery in zip(numbers_row,
                                                                                      numbers_order,
                                                                                      cost_in_dollars,
                                                                                      delivery_time,
                                                                                      statuses_delivery,
                                                                                      ):
        datas = (int(number), int(numbers_order), int(cost_in_dollars), delivery_time,
                 int(cost_in_dollars) * get_central_bank_rate(), status_delivery)
        datas_for_db.append(datas)

    return datas_for_db


def get_central_bank_rate():
    """We get the exchange rate of the Central Bank of the ruble to the dollar"""
    url_response = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url_response)
    json = response.json()

    dollar_exchange_rate = json['Valute']['USD']['Value']

    return dollar_exchange_rate


def main():
    """The function is responsible for launching the main application"""
    while True:
        print(LogPhrases.CHECK)
        db = DataBase(get_columns_google_table())

        if 'orders' in db.get_tables():
            print(LogPhrases.LOG_NOW.format(datetime.now()))
            db.checking_tables()
        else:
            print(LogPhrases.TABLE_NOT_FOUND)
            db.create_table()

        time.sleep(30)


if __name__ == '__main__':
    print(LogPhrases.HELLO)
    Thread(target=main).start()
    Thread(target=bot.polling(non_stop=True)).start()
