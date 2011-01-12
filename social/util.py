from shade.social.models import UserProfile
import random, string, datetime

def gen_url():
    chars = string.letters + string.digits
    url = ''
    for i in range(20):
        url += random.choice(chars)

    conflicts = UserProfile.objects.filter(url=url)
    if conflicts:
        return gen_url()

    return url

def can_users_interract(user1, user2):
    return (user1 == user2 or user1 in user2.get_profile().friends.all())

def get_age(birthdate):
    if not birthdate:
        return None

    today = datetime.date.today()
    age = today.year - birthdate.year

    #Find this years birthday
    bday = datetime.date(month=birthdate.month, day=birthdate.day, year=today.year)
    if (today - bday).days < 0:
        age = age - 1

    return age

