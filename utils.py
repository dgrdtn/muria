import random
import secrets
import requests
import ast
import json
import time
from datetime import datetime


first_names = open('data/first_names.txt').readlines()
last_names = open('data/last_names.txt').readlines()
passwords = open('data/passwords.txt', encoding="utf8").readlines()
passwords = [pwd.strip() for pwd in passwords]
usernames = open('data/usernames.txt').readlines()

def get_random_first_name():
    return random.choice(first_names).replace('\n', '')

def get_random_last_name():
    return random.choice(last_names).replace('\n', '')

def get_random_password():
    return random.choice(passwords).replace('\n', '') + 'Ab1!'

def get_random_username():
    return random.choice(usernames).replace('\n', '')


def get_private_key():
    return "0x" + secrets.token_hex(32)

def get_message_for_metamask():
    time_url = "https://myriaverse-api.myria.com/v1/time"
    time = ast.literal_eval(requests.get(time_url).text)["data"]["time"]
    return "{\"created_on\":\"" + time + "\"}"


def get_random_alliance():
    return "equinox"


def get_link_from_email(user):
    data = None
    while data is None or len(data) == 0:
        print("Getting link from email...")
        try:
            resp = requests.get("http://cozzymail.ru/mail", json={
                "to": user.email
            }, timeout=15)
        except:
            print("    Connection aborted")
            continue

        if resp.status_code == 200:
            data = json.loads(resp.text)
        else:
            print("    Email is not received yet..Sleeping")
            time.sleep(5)
    print("Done!")
    return data