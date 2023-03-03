import const
import json
import requests
import time
from datetime import datetime

# TODO trace all requests (if two within 5 sec, now replies to last only). def new_request => True, for while loop
# TODO check if chat id in saved list and handle (multiple users)
# TODO when getting request - take chat id and reply to this chat id


# timezone setup
def get_location():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()['ip']
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = f'{response.get("city")}, {response.get("country_name")}'
    return location_data


def get_time(city):
    try:
        response = requests.get(const.TZ_URL.format(KEY=const.PRIMARY_KEY, city=city.title())).text
        content = json.loads(response)
        time_there = datetime.strptime(content['datetime'], '%Y-%m-%d %H:%M:%S').time().replace(second=0, microsecond=0)
        time_here = datetime.now().time().replace(second=0, microsecond=0)
        current_location = get_location()
        info = f"In {city.title()} time now is {time_there}\n" \
               f"You are now in {current_location}, and its {time_here}\n" \
               f"Time difference is {(time_here.hour - time_there.hour)}.{time_here.minute - time_there.minute} hours"
        return info
    except KeyError:
        return "Probably this will help: https://maps.google.com"


def reply_to_bot(data):
    data_post = {
        'chat_id': const.CHAT_ID,
        'text': data
    }
    url = const.URL.format(TOKEN=const.TOKEN, method=const.SEND)
    requests.request('POST', url, params=data_post)


def get_city(data):
    city = data['message']['text']
    return city.title()


def save_update_id(data):
    with open(const.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(data['update_id']))
    const.UPDATE_ID = data['update_id']


def main():
    while True:
        # checking if there is any requests in bot
        response = requests.get(const.URL.format(TOKEN=const.TOKEN, method=const.UPDATES)).text
        json_content = json.loads(response)
        data = json_content
        print(data)
        needed_part = None

        # getting last request for my chat
        for res in data['result']:
            if res['message']['chat']['id'] == const.CHAT_ID:
                needed_part = res

        # checking if request is fresh (unreplied)
        if const.UPDATE_ID != needed_part['update_id']:
            city = get_city(needed_part)
            time_now = get_time(city)
            reply_to_bot(time_now)
            save_update_id(needed_part)

        time.sleep(5)


if __name__ == '__main__':
    main()
