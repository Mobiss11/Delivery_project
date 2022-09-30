class CommandDb:
    COMMAND_CREATE_TABLE = '''CREATE TABLE ORDERS  
             (NUMBER INT PRIMARY KEY NOT NULL,
             NUMBER_ORDER INT NOT NULL,
             COST_IN_DOLLARS INT NOT NULL,
             DELIVERY_TIME CHAR(10),
             COST_IN_RUBLES FLOAT NOT NULL,
             STATUS_DELIVERY CHAR(15));'''

    COMMAND_INSERT = '''INSERT INTO orders 
                    (number, number_order, cost_in_dollars, delivery_time, cost_in_rubles, status_delivery) 
                    VALUES{}'''
    COMMAND_INSERT_NEW_POST = '''INSERT INTO orders 
                                  (number, number_order, cost_in_dollars, delivery_time, cost_in_rubles, 
                                  status_delivery) 
                                  VALUES(%s,%s,%s,%s,%s,%s)'''

    COMMAND_SELECT_TABLES_DB = 'SELECT tablename FROM pg_catalog.pg_tables;'
    COMMAND_SELECT_ORDERS = 'SELECT * FROM orders;'
    COMMAND_SELECT_COUNT_ORDERS = 'SELECT count (*) FROM orders;'
    COMMAND_SELECT_POST = 'SELECT * FROM orders WHERE number = %s'
    COMMAND_SELECT_NUMBERS_ORDERS = 'SELECT number_order FROM orders'
    COMMAND_SELECT_STATUSES_DELIVERY_TIME = 'SELECT status_delivery FROM orders where number_order = %s'

    COMMAND_UPDATE_POST_NUMBER_ORDER = 'Update orders set number_order = %s where number = %s'
    COMMAND_UPDATE_POST_COST_DOLLARS = 'Update orders set cost_in_dollars = %s where number = %s'
    COMMAND_UPDATE_POST_DELIVERY_TIME = 'Update orders set delivery_time = %s where number = %s'
    COMMAND_UPDATE_POST_COST_RUBLES = 'Update orders set cost_in_rubles = %s where number = %s'
    COMMAND_UPDATE_STATUS_DELIVERY_TIME = 'Update orders set status_delivery = %s where number = %s'

    COMMAND_DELETE_POST = 'Delete from orders where number = %s'


class LogPhrases:

    # Main app
    CREATE_TABLE = 'Table created successfully'
    LOG_NOW = 'All data checked or updated - {}'
    TABLE_NOT_FOUND = 'Table not found, please wait, now create new table db... '
    HELLO = 'Hi, now checking table db - orders'
    CHECK = 'Now there is a check'

    # Telegram bot
    CHANGE_DELIVERY_TIME_TG = 'По заказу {} Изменилась дата поставки с {} на {}'
    HELLO_TELEGRAM = 'Добро пожаложвать в бот - умный пощник, что я умею:' \
                     '\n\n-Оповещать если срок поставки измениться\n-Проверять соблюдение сроков поставки,'
    NUMBER_ORDER_TG = 'Введите номер заказа, например 1135907'
    BUTTON_CHECK_TG = 'Проверить соблюдение сроков'
    STATUS_DELIVERY_TG = 'Статус поставки по заказу {} - {}'
