from models import User
import jwt
from utils import *
from web3.auto import w3
from eth_account.messages import encode_defunct
from hexbytes import HexBytes

login_url = "https://myriaverse-api.myria.com/v1/accounts/login/wallet"
alliance_url = "https://myriaverse-api.myria.com/v1/sigil/users/alliance"
profile_url = "https://myriaverse-api.myria.com/v1/sigil/users/profile"
link_url = "https://myriaverse-api.myria.com/v1/accounts/link"


def add_metamask(user, session):
    print("Generating metamask..")
    msg = get_message_for_metamask()
    message = encode_defunct(text=msg)
    signed_message = w3.eth.account.sign_message(message, private_key=user.private_key)
    signature = HexBytes(signed_message.signature).hex()
    payload = {
        "message": msg,
        "signature": signature,
        "wallet_id": user.wallet.address
    }
    r = session.post(login_url, data=payload)
    success = r.status_code == 200
    print(f"    Success: {success}")
    user.access_token = session.cookies.get_dict()["access_token"]
    user.session = session.cookies.get_dict()["session"]
    user.id = jwt.decode(user.access_token, options={"verify_signature": False}, algorithms=["HS256"])['user_id']
    return success


def select_alliance(user, session):
    print('Select alliance')
    user.alliance = get_random_alliance()
    payload = {
        "alliance_id": user.alliance
    }
    success = False

    response = session.get(profile_url)
    if response.status_code == 200:
        response = session.post(alliance_url, json=payload)
        success = response.status_code == 200
        print(f'    Success: {success}')
    return success


def complete_account(user, session, referral_code=None):
    print("Creating account..")
    payload = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "redirect": 0,
        "username": user.username
    }
    if referral_code:
        payload['referral_code'] = referral_code
    response = session.post(link_url, data=payload)

    success = response.status_code == 200
    print(f"    Success: {success}")
    return success
