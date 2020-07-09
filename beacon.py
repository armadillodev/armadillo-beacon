#!/usr/bin/env python3

import json
import urllib.request
from urllib.error import URLError
import random
import time

domain = "localhost"
api_path = "/api/data"
port = 8000

url = f'http://{domain}:{port}{api_path}'
trailor_id = 1


def make_packet(temp):
    data = {
        "trailor": trailor_id,
        "temperature": temp,
    }

    return json.dumps(data)

def send_data(data):
    headers = {
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data.encode('utf-8'), headers=headers)
    try: 
        urllib.request.urlopen(req)
    except URLError as err:
        print('failed to send data')
        print(err)

def get_random_temp():
    return random.choice(range(10, 40))


def main():
    print('starting armadillo beacon')
    print(f'sending to: {url}')

    while True:
        temp = get_random_temp()
        data = make_packet(temp)
        send_data(data)
        print(f'sent: "{data}"')

        time.sleep(1)


if __name__ == '__main__': main()
