from shade.social.models import User

def my_user(request):
    try:
        my_user = request.session['user']
        return {'my_user': my_user}
    except KeyError:
        return {}

