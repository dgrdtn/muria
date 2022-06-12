from user_autoreg import *
import jwt
import threading

INVITE_CODE = "a77f0941-7561-4a0f-837e-71b591590d07"
#

# user = User("pisanac970@cozzymail.ru")
# r1 = add_metamask(user, s)
#
# select_alliance(user, s)
# r3 = complete_account(user, s)
#
# #
# token = s.cookies.get_dict()["access_token"]
# access_token = cookie["access_token"]

# test = jwt.decode(access_token, options={"verify_signature": False}, algorithms=["HS256"])


def register_new_user():
    s = requests.session()
    s.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'origin': 'https://myria.com',
        'referer': 'https://myria.com/'
    })
    user = User()
    success = add_metamask(user, s)
    if not success:
        return

    success = select_alliance(user, s)
    if not success:
        return

    success = complete_account(user, s, referral_code=INVITE_CODE)
    if not success:
        return
    # a = 1
    data = get_link_from_email(user)
    msg = data[0]['message']

    keyword_1 = "Please click the below url to verify your registration:"
    keyword_2 = "=0"

    url_start_index = msg.find(keyword_1) + len(keyword_1)
    url_end_index = msg.find(keyword_2, url_start_index) + len(keyword_2)
    link = msg[url_start_index:url_end_index].strip()

    print("Activating account..")
    response = s.get(link)
    if response.status_code == 200:
        print("    Done!")
    else:
        print("Failed to open the link")
    print("=========================================================")


def register_150_users():
    for i in range(0, 150):
        register_new_user()


for i in range(50):
    t = threading.Thread(target=register_150_users)
    t.start()