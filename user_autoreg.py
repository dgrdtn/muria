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
    token = session.cookies.get_dict()["access_token"]
    user.id = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])['user_id']
    return r

def select_alliance(user, session):
    user.alliance = get_random_alliance()
    payload = {
        "alliance": user.alliance
    }
    session.get(profile_url)
    return session.post(alliance_url, data=payload)

def complete_account(user, session, referral_code = None):
    payload = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "redirect": 0,
        "username": user.username
    }
    if referral_code:
        payload.update({'referral_code': referral_code})
    return session.post(link_url, data=payload)
