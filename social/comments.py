from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core import serializers
from django.forms.models import model_to_dict
import forms as myforms
import util
from .models import UserProfile, Comment, SubComment
from .groups import GroupUpdates
import datetime, json

def comment_to_dict(comment):
    c = {}
    c['id'] = comment.pk
    c['author'] = comment.author.first_name + ' ' + comment.author.last_name
    c['text'] = comment.post
    c['sent'] = str(comment.sent)
    return c

def comments(request):
    now = datetime.datetime.now()
    week = datetime.timedelta(days=7)
    last_week = now - week
    user = request.user
    updates = []
    # Add user's status updates and comments from friends to user
    my_comments = user.userprofile.comments.filter(sent__gte=last_week)
    up = []
    for c in my_comments:
        cd = comment_to_dict(c)
        cd['sub'] = [comment_to_dict(x) for x in c.subcomments.all()]
        up.append(cd)
    #up = serializers.serialize('json', up)
    #me = {'Me': up}
    #me = GroupUpdates()
    #me.name = 'Me'
    #me.updates = up
    #updates.append(me)
    updates.extend(up)

    # Add user's friends' status updates
    
    friends = list(user.userprofile.friends.all())
    subs = list(user.userprofile.subscriptions.all())
    '''
    groups = user.userprofile.groups.all()
    for g in groups:
        up = []
        members = g.members.all()
        for f in members:
            us = f.userprofile.comments.filter(author=f, sent__gte=last_week)
            for u in us:
                cd = comment_to_dict(c)
                cd['sub'] = [comment_to_dict(x) for x in c.subcomments.all()]
                up.append(u)
            f = User.objects.get(username=f)
            # Remove f from list, so they don't end up in uncategorized
            friends.remove(f)
        up.sort(key=lambda x: x.sent, reverse=True)
        #up = serializers.serialize('json', up)
        gu = {g: up}
        #gu = GroupUpdates()
        #gu.name = g
        #gu.updates = up
        #updates.extend(gu)
    '''
    #reset up in case friends is empty
    up = []
    for f in friends:
        comments = f.userprofile.comments.filter(sent__gte=last_week)
        for c in comments:
            cd = comment_to_dict(c)
            cd['sub'] = [comment_to_dict(x) for x in c.subcomments.all()]
            up.append(cd)
    #ungrouped subscriptions
    #for s in subs:
        #make sure public=True, we don't want to leak private updates.
    #    comments = s.userprofile.comments.filter(public=True, sent__gte=last_week)
    #    for c in comments:
    #        up.append(c)

    #up.sort(key=lambda x: x.sent, reverse=True)
    #up = serializers.serialize('json', up)
    #ng = {'No Group': up}
    #ng = GroupUpdates()
    #ng.name = 'No Group'
    #ng.updates = up
    updates.extend(up)
    return JsonResponse(updates, safe=False)

@login_required
def post(request, url):
    user = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user

    if util.can_users_interract(user, other_user):
        if request.method == 'POST':
            comment = Comment.objects.create(
                    author=user,
                    read=False,
                    sent = datetime.datetime.now()
                    )
            form = myforms.CommentForm(request.POST, instance=comment)
            comment = form.save()
            other_user.userprofile.comments.add(comment)
    return HttpResponseRedirect('/dashboard/')

@login_required
def reply(request, url, comment_id):
    user = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user

    if request.method == 'POST':
        if util.can_users_interract(user, other_user):
            comment = get_object_or_404(Comment, id=comment_id)
            subcomment = SubComment.objects.create(
                    author=user,
                    post=request.POST['post'],
                    read=False,
                    sent=datetime.datetime.now(),
                    parent=comment,
                    )
            comment.subcomments.add(subcomment)

    return HttpResponseRedirect('/profile/'+other_user.userprofile.url)

@login_required
def delete(request, url, comment_id):
    prof = request.user.userprofile
    comment = Comment.objects.get(id=comment_id)
    if comment in prof.comments.all():
        prof.comments.remove(comment)
        comment.delete()

    return HttpResponseRedirect('/dashboard/')

