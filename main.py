from user_autoreg import *
import jwt


#
s = requests.session()
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
user = User("dave444@cozzymail.ru")
add_metamask(user, s)
select_alliance(user, s)
r = complete_account(user, s)
# a = 1
b = get_link_from_email(user)
# user2 = User("feasdasdasd")
# user.save_as_main()
# user.save_as_referral(user)
a = 1


