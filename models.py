import json
import os.path
import random
from utils import *
from eth_account import Account

class User:

    def __init__(self, email=None):
        self.first_name = get_random_first_name()
        self.last_name = get_random_last_name()
        self.password = get_random_password()
        self.username = get_random_username()
        if email is None:
            self.email = self.first_name[0] + self.last_name[0] + str(random.randint(10, 100)) + '@cozzymail.ru'

        self.alliance = None
        self.id = None
        self.access_token = None
        self.session = None

        self.private_key = get_private_key()
        self.wallet = Account.from_key(self.private_key)

    def to_dict(self):
        d = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'username': self.username,
            'email': self.email,
            'alliance': self.alliance,
            'user_id': self.id,
            'private_key': self.private_key,
            'wallet': self.wallet.address
        }
        return d


    def save_as_main(self):
        dst_folder = os.path.join("Accounts")
        if not os.path.exists(dst_folder):
            os.mkdir(dst_folder)

        file_path = os.path.join(dst_folder, self.wallet.address)
        with open(file_path, 'w', encoding='utf-16') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def save_as_referral(self, user):
        dst_folder = os.path.join("Referrals", user.wallet.address)
        if not os.path.exists(dst_folder):
            os.mkdir(dst_folder)

        file_path = os.path.join(dst_folder, self.wallet.address)
        with open(file_path, 'w', encoding='utf-16') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)







