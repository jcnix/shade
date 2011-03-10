from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from shade.social import forms as myforms
from shade.social.models import UserProfile, Message
import datetime

@login_required
def inbox(request):
    return render_to_response('messages/inbox.html', {},
            context_instance=RequestContext(request))

@login_required
def msg_view(request, msg_id):
    user = request.user
    m = get_object_or_404(Message, pk=msg_id)
    # Don't allow just anyone to read messages
    if m not in user.get_profile().messages.all():
        return HttpResponseRedirect('/')
    else:
        if not m.read:
            m.read = True
            m.save()
        return render_to_response('messages/view.html', {'msg': m},
                context_instance=RequestContext(request))

@login_required
def msg_compose(request, msg_id=0):
    user = request.user
    if request.method == 'POST':
        now = datetime.datetime.now()
        msg = Message(author=user, sent=now)
        form = myforms.MessageForm(request.POST, instance=msg)
        if form.is_valid():
            m = form.save()
            recipient = form.cleaned_data['recipient']
            recipient.get_profile().messages.add(m)
            recipient.get_profile().save()
            return HttpResponseRedirect('/inbox/')

    # replying
    if msg_id > 0:
        m = Message.objects.get(id=msg_id)
        subject = 'Re: '+m.subject
        msg = Message(recipient=m.author, subject=subject)
        form = myforms.MessageForm(instance=msg)
    else:
        return HttpResponseRedirect('/inbox/')
    form.fields['recipient'].choices = ((u.id, u.get_full_name()) for u in user.get_profile().friends.all())
    return render_to_response('messages/compose.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def msg_delete(request, msg_id):
    user = request.user
    msg = Message.objects.get(id=msg_id)
    if msg in user.get_profile().messages.all():
        user.get_profile().messages.remove(msg)
        msg.delete()
    return HttpResponseRedirect('/inbox')

