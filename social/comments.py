from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from shade.social import forms as myforms
from shade.social import util
from shade.social.models import UserProfile, Comment, SubComment
import datetime

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
            other_user.get_profile().comments.add(comment)
    return HttpResponseRedirect('/profile/'+other_user.get_profile().url+'/')

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

    return HttpResponseRedirect('/profile/'+other_user.get_profile().url)

@login_required
def delete(request, url, comment_id):
    prof = request.user.get_profile()
    comment = Comment.objects.get(id=comment_id)
    if comment in prof.comments.all():
        prof.comments.remove(comment)
        comment.delete()

    return HttpResponseRedirect('/dashboard/')

