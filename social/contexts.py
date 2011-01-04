from shade.social.models import Message

def unread_message_count(request):
    u = request.user
    m = Message.objects.filter(recipient=u, read=False).count()
    return {'unread_msg_count': m}

