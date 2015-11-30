from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import forms as myforms
from .models import UserProfile, Message
import datetime

@login_required
def inbox(request):
    return render_to_response('messages/inbox.html', {'nbar': 'inbox'},
            context_instance=RequestContext(request))

@login_required
def msg_view(request, msg_id):
    user = request.user
    m = get_object_or_404(Message, pk=msg_id)
    # Don't allow just anyone to read messages
    if m not in user.userprofile.messages.all():
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
    form = myforms.MessageForm()
    if request.method == 'POST':
        now = datetime.datetime.now()
        msg = Message(author=user, sent=now, read=False)
        form = myforms.MessageForm(request.POST, instance=msg)
        if form.is_valid():
            m = form.save()
            recipient = form.cleaned_data['recipient']
            recipient.userprofile.messages.add(m)
            recipient.userprofile.save()
            return HttpResponseRedirect('/inbox/')

    # replying
    if msg_id > 0:
        m = Message.objects.get(id=msg_id)
        subject = 'Re: '+m.subject
        msg = Message(recipient=m.author, subject=subject)
        form = myforms.MessageForm(instance=msg)

    form.fields['recipient'].choices = ((u.id, u.get_full_name()) for u in user.userprofile.friends.all())
    return render_to_response('messages/compose.html', {'form': form, 'nbar': 'compose'},
            context_instance=RequestContext(request))

@login_required
def msg_delete(request, msg_id):
    user = request.user
    msg = Message.objects.get(id=msg_id)
    if msg in user.userprofile.messages.all():
        user.userprofile.messages.remove(msg)
        msg.delete()
    return HttpResponseRedirect('/inbox')

