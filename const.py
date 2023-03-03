# telegram
TOKEN = '6161418154:AAGas7JQMFJfUlpVSE0ri9AQLvPdRzH-n9o'
URL = 'http://api.telegram.org/bot{TOKEN}/{method}'

UPDATES = 'getUpdates'
SEND = 'sendMessage'
CHAT_ID = 1863210850

UPDATE_ID_FILE_PATH = 'update_id'

with open(UPDATE_ID_FILE_PATH) as file:
    data = file.readline()
    if data:
        UPDATE_ID = data

# timezone
PRIMARY_KEY = '57fa8899696c44e9a3a0219001f5afbf'
TZ_URL = 'https://timezone.abstractapi.com/v1/current_time/?api_key={KEY}&location={city}'
