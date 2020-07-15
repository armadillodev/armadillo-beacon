#!/usr/bin/env python3

import json
import urllib.request
from urllib.error import URLError
import random
import time

class Config:
    def __init__(self, url, bikes):
        self.url = url
        self.bikes = bikes

def read_config():
    with open('config.json') as file:
        file_data = json.loads(file.read())

        servers = file_data['servers']
        print(servers)
        target = input('which server: ')

        domain = servers[target]['domain']
        api_path = servers[target]['api_path']
        port = servers[target]['port']

        config = Config(
            f'http://{domain}:{port}{api_path}',
            file_data['bikes']
        )
        return config


def create_random_bike_data():
    current = random.choice(range(10, 40))
    voltage = random.choice(range(10, 40))
    rpm = random.choice(range(10, 40))

    data = {
        "current": current,
        "voltage": voltage,
        "rpm": rpm,
    }

    return json.dumps(data)

def send_bike_data(url, bike_id, data):
    headers = {
        "Content-Type": "application/json",
    }

    url = f'{url}/bike/{bike_id}'
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data, headers=headers)

    try:
        urllib.request.urlopen(req)
    except URLError as err:
        print('failed to send data')
        print(err)

def create_random_bike_sender(url):
    def send(bike_id):
        data = create_random_bike_data()
        print(f'sending: {data}')
        send_bike_data(url, bike_id, data)

    return send

def main():
    print('starting armadillo beacon')

    config = read_config()

    print(f'sending to: {config.url}')
    print(f'bikes: {config.bikes}')

    bike_sender = create_random_bike_sender(config.url)

    while True:
        for bike in config.bikes:
            bike_sender(bike)

        time.sleep(1)


if __name__ == '__main__': main()
