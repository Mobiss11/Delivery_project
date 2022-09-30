import psycopg2

from telegram import send_change_delivery_time
from config import database, user, password, host, port
from constants import CommandDb, LogPhrases

data_base = psycopg2.connect(
    database=database,
    user=user,
    password=password,
    host=host,
    port=port
)
cursor = data_base.cursor()


class DataBase:
    """The class is working with the database.
    In the constructor we get a tuple with Google table data
    """
    def __init__(self, info_from_google_table):
        self.info_google = info_from_google_table

    def create_table(self):
        """The method in which we create a table in the database  and
        fill the table with data, if there is no such table
        """
        cursor.execute(CommandDb.COMMAND_CREATE_TABLE)
        data_base.commit()

        data_records = ", ".join(["%s"] * len(self.info_google))
        insert_query = CommandDb.COMMAND_INSERT.format(data_records)

        cursor.execute(insert_query, self.info_google)
        data_base.commit()
        print(LogPhrases.CREATE_TABLE)

    @staticmethod
    def get_tables():
        """A static method in which we get all the tables from the database"""
        cursor.execute(CommandDb.COMMAND_SELECT_TABLES_DB)
        tables = cursor.fetchall()
        tables_to_check = []

        for table in tables:
            tables_to_check.append(table[0])

        return tables_to_check

    def checking_tables(self):
        """The method in which we check the records in the table"""
        cursor.execute(CommandDb.COMMAND_SELECT_COUNT_ORDERS)
        count_row_tables_db = cursor.fetchall()
        count_row_tables_google = len(self.info_google)

        if count_row_tables_google < count_row_tables_db[0][0]:
            self.delete_post()

        if count_row_tables_google > count_row_tables_db[0][0]:
            self.insert_new_post()

        if count_row_tables_google == count_row_tables_db[0][0]:
            self.change_post()

    def insert_new_post(self):
        """The method in which we insert a new record"""
        cursor.execute(CommandDb.COMMAND_SELECT_ORDERS)
        table_db_orders = cursor.fetchall()

        numbers_orders_db_orders = []

        for element_db in table_db_orders:
            numbers_orders_db_orders.append(element_db[1])

        for element_google in self.info_google:
            if element_google[1] not in numbers_orders_db_orders:
                datas = (
                    element_google[0],
                    element_google[1],
                    element_google[2],
                    element_google[3],
                    element_google[4],
                    element_google[5],
                )
                cursor.execute(CommandDb.COMMAND_INSERT_NEW_POST, datas)
                data_base.commit()

    def delete_post(self):
        """The method in which we delete the record"""
        cursor.execute(CommandDb.COMMAND_SELECT_ORDERS)
        table_db_orders = cursor.fetchall()

        numbers_orders_google_table = []

        for element_google in self.info_google:
            numbers_orders_google_table.append(element_google[1])

        for element_db in table_db_orders:
            if element_db[1] not in numbers_orders_google_table:
                cursor.execute(CommandDb.COMMAND_DELETE_POST, (element_db[0],))
                data_base.commit()

    def change_post(self):
        """The method in which we change the record"""
        for element_google in self.info_google:
            cursor.execute(CommandDb.COMMAND_SELECT_POST, (element_google[0],))
            post = cursor.fetchone()

            if element_google[1] != post[1]:
                cursor.execute(CommandDb.COMMAND_UPDATE_POST_NUMBER_ORDER, (element_google[1], element_google[0]))
                data_base.commit()

            if element_google[2] != post[2]:
                cursor.execute(CommandDb.COMMAND_UPDATE_POST_COST_DOLLARS, (element_google[2], element_google[0]))
                data_base.commit()

            if element_google[3] != post[3]:
                cursor.execute(CommandDb.COMMAND_UPDATE_POST_DELIVERY_TIME, (element_google[3], element_google[0]))
                data_base.commit()

                send_change_delivery_time(element_google[1], post[3], element_google[3])

            if element_google[4] != post[4]:
                cursor.execute(CommandDb.COMMAND_UPDATE_POST_COST_RUBLES, (element_google[4], element_google[0]))
                data_base.commit()

            if element_google[5] != post[5]:
                cursor.execute(CommandDb.COMMAND_UPDATE_STATUS_DELIVERY_TIME, (element_google[5], element_google[0]))
                data_base.commit()
