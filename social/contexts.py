from shade.social.models import Message
import datetime

def upcoming_events(request):
    if request.user.is_authenticated():
        now = datetime.datetime.now()
        user = request.user
        events = user.userprofile.events.filter(datetime__gte=now)
    else:
        events = None
    return {'upcoming_events': events}

def unread_message_count(request):
    if request.user.is_authenticated():
        u = request.user
        m = Message.objects.filter(recipient=u, read=False).count()
    else:
        m = None
    return {'unread_msg_count': m}

