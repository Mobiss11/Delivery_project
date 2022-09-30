from dotenv import dotenv_values
import gspread

config = dotenv_values('.env')

# Settings GoogleTable
google_credentials = gspread.service_account(filename='credentials.json')
google_sheet = google_credentials.open_by_url(config['URL_TABLE'])
sheet_with_data = google_sheet.worksheet(config['WORKSHEET'])

# Settings DataBase
database = config['DATABASE']
user = config['USER']
password = config['PASSWORD']
host = config['HOST']
port = config['PORT']

# Settings TelegramBot
telegram_token = config['TOKEN_TELEGRAM']
telegram_users = [792818131, ]
