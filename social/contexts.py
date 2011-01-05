from shade.social.models import Message

def unread_message_count(request):
    if request.user.is_authenticated():
        u = request.user
        m = Message.objects.filter(recipient=u, read=False).count()
    else:
        m = None
    return {'unread_msg_count': m}

