from shade.social.models import UserProfile
import random, string

def gen_url():
    chars = string.letters + string.digits
    url = ''
    for i in range(20):
        url += random.choice(chars)

    conflicts = UserProfile.objects.filter(url=url)
    if conflicts:
        return gen_url()

    return url

