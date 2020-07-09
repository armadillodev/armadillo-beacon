#!/usr/bin/env python3

import json
import urllib.request
from urllib.error import URLError
import random
import time

class Config:
    def __init__(self, url, trailor_id):
        self.url = url
        self.trailor_id = trailor_id

def read_conf():
    with open('config.json') as file:
        file_data = json.loads(file.read())

        domain = file_data['domain']
        api_path = file_data['api_path']
        port = file_data['port']

        config = Config(
            f'http://{domain}:{port}{api_path}',
            file_data['trailor_id']
        )
        return config


def make_packet(trailor_id, temp):
    data = {
        "trailor": trailor_id,
        "temperature": temp,
    }

    return json.dumps(data)

def send_data(url, data):
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

    config = read_conf()

    print(f'sending to: {config.url}')
    print(f'trailor id: {config.trailor_id}')

    while True:
        temp = get_random_temp()
        data = make_packet(config.trailor_id, temp)
        send_data(config.url, data)
        print(f'sent: "{data}"')

        time.sleep(1)


if __name__ == '__main__': main()
