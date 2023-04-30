import json
import time
import argparse
from datetime import datetime
import requests
from difflib import SequenceMatcher

from modules import io_driver
from modules.io_driver import *
from modules.mailer import *
import config

URL = config.RESPONSECHECK_URL
driver: IODriver = None

def get_response_text(URL):
    try:
        response = requests.get(URL)
        if response.status_code != 200:
            raise Exception(f"Request returned with status {response.status_code}")
        text = response.text
        return text
    except Exception as e:
        raise e


def has_changed(new, original):
    similarity = SequenceMatcher(None, new, original).ratio()
    return similarity <= config.DIFF_THRESHOLD, similarity


def main():
    global URL, driver

    parser = argparse.ArgumentParser(
        description="Periodically calculates the checksums of content in a specified directory and alerts through email if there are changes")
    parser.add_argument(
        "command", help="The operation to carry out, update updates the current hashes, run performs periodic checks", choices=['update', 'run'], type=str)
    args = parser.parse_args()

    io_driver.ADAFRUIT_IO_FEED_NAME = "DefaceCheckResponseCheck"
    io_driver.ADAFRUIT_IO_FEED_KEY = "defacecheckresponsecheck"

    if config.IO_DRIVER == 'file':
        driver = FileDriver()
    elif config.IO_DRIVER == 'adafruit':
        driver = AdafruitIODriver()
    else:
        raise Exception("Unrecognized IODriver")

    try:
        if args.command == 'run':
            run()
        elif args.command == 'update':
            update()
    except KeyboardInterrupt:
        pass


def run():
    print("Program is now scanning, press Ctrl+C to stop")
    while True:
        check()
        time.sleep(config.SCAN_INTERVAL * 60)


def check():
    global URL, driver

    new_response = get_response_text(URL)
    old_response = driver.read_from()
    
    v_has_changed, similarity = has_changed(new_response, old_response)
    if v_has_changed:
        print(f"[{datetime.now()}] Scan finished, changes detected")
        print(f"[{datetime.now()}] Similarity of {similarity}, minimum threshold was {config.DIFF_THRESHOLD}")
        send_alert_email()
        exit()
    else:
        print(f"[{datetime.now()}] Scan finished, no changes found")
        print(f"[{datetime.now()}] Similarity of {similarity}, minimum threshold was {config.DIFF_THRESHOLD}")


def update():
    global URL, driver

    response = get_response_text(URL)
    driver.write_to(response)


if __name__ == '__main__':
    main()
