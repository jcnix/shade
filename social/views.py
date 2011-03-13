from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from shade.social import forms as myforms
from shade.social import util
from shade.social.models import UserProfile, Language, Invite, Message
from shade.social.models import Comment, SubComment, Album, Picture, Event
from shade.social.models import EventInvite, Group
import hashlib, datetime

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login')

@login_required
def dashboard(request):
    now = datetime.datetime.now()
    week = datetime.timedelta(days=7)
    last_week = now - week
    user = request.user

    updates = {}
    # Add user's status updates and comments from friends to user
    my_comments = user.get_profile().comments.filter(sent__gte=last_week)
    up = []
    for c in my_comments:
        up.append(c)
    updates['Me'] = up

    # Add user's friends' status updates
    friends = list(user.get_profile().friends.all())
    subs = list(user.get_profile().subscriptions.all())
    groups = user.get_profile().groups.all()
    for g in groups:
        updates[g] = None
        up = []
        members = g.members.all()
        for f in members:
            us = f.get_profile().comments.filter(author=f, sent__gte=last_week)
            for u in us:
                up.append(u)
            f = User.objects.get(username=f)
            friends.remove(f)
        up.sort(key=lambda x: x.sent, reverse=True)
        updates[g] = up

    #reset up in case friends is empty
    up = []
    for f in friends:
        comments = f.get_profile().comments.filter(sent__gte=last_week)
        for c in comments:
            up.append(c)
    #ungrouped subscriptions
    for s in subs:
        #make sure public=True, we don't want to leak private updates.
        comments = s.get_profile().comments.filter(public=True, sent__gte=last_week)
        for c in comments:
            up.append(c)

    up.sort(key=lambda x: x.sent, reverse=True)
    updates['No Group'] = up

    form = myforms.CommentForm()
    return render_to_response('dashboard.html', {'updates': updates, 'form': form},
            context_instance=RequestContext(request))

@login_required
def settings(request):
    #save this in case the url is invalid
    old_url = request.user.get_profile().url
    form = myforms.SettingsForm(instance=request.user.get_profile())

    if request.method == 'POST':
        form = myforms.SettingsForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
        else:
            # if the url is invalid, the session user will still
            # try to use the invalid url, so we need to reload
            # the session user from the database.
            profile = UserProfile.objects.get(url=old_url)
            request.user = profile.user

    return render_to_response('settings/settings.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def manage_friends(request):
    return render_to_response('settings/friends.html', {},
            context_instance=RequestContext(request))

@login_required
def manage_friend(request, id):
    other_user = get_object_or_404(User, pk=id)
    return render_to_response('settings/friend.html', {'friend': other_user},
            context_instance=RequestContext(request))

@login_required
def new_group(request):
    user = request.user
    if request.method == 'POST':
        form = myforms.GroupForm(request.POST, user=user)
        if form.is_valid():
            g = form.save()
            user.get_profile().groups.add(g)
            return HttpResponseRedirect('/settings/friends/')

    form = myforms.GroupForm(user=user)
    return render_to_response('settings/group.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def edit_group(request, id):
    group = Group.objects.get(id=id)
    user = request.user
    if request.method == 'POST':
        form = myforms.GroupForm(request.POST, instance=group, user=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings/friends/')

    form = myforms.GroupForm(instance=group, user=user)
    return render_to_response('settings/group.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def change_pass(request):
    form = myforms.ChangePassForm()
    if request.method == 'POST':
        form = myforms.ChangePassForm(request.POST)
        if form.is_valid():
            user = request.user
            if not auth.models.check_password(form.cleaned_data['old_pass'], user.password):
                form._errors['old_pass'] = [u'Old password is incorrect']
            else:
                user.set_password(form.cleaned_data['new_pass1'])
                user.save()
                return HttpResponseRedirect('/dashboard/')

    return render_to_response('settings/change_pass.html', {'form': form},
            context_instance=RequestContext(request))

def profile(request, url):
    user = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user

    form = None
    age = None
    invited = False

    if user.is_authenticated():
        #check if we've invited the user to be our friend
        try:
            inv = other_user.get_profile().invites.get(sender=user)
            invited = True
        except Invite.DoesNotExist:
            invited = False

        age = util.get_age(other_user.get_profile().birthdate)

        # post a comment
        if util.can_users_interract(user, other_user):
            form = myforms.CommentForm()
        else:
            form = None

    return render_to_response('profile/profile.html', {'other_user': other_user, 
        'form': form, 'invited': invited, 'age': age},
        context_instance=RequestContext(request))

@login_required
def post_comment(request, url):
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
def reply_to_comment(request, url, comment_id):
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
def delete_comment(request, url, comment_id):
    prof = request.user.get_profile()
    comment = Comment.objects.get(id=comment_id)
    if comment in prof.comments.all():
        prof.comments.remove(comment)
        comment.delete()

    return HttpResponseRedirect('/dashboard/')

@login_required
def subscribe(request, url):
    user = request.user
    prof = user.get_profile()
    other_user_prof = UserProfile.objects.get(url=url)
    other_user = other_user_prof.user
    prof.subscriptions.add(other_user)

    return HttpResponseRedirect('/dashboard/')

@login_required
def albums(request, url):
    user = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user
    if other_user == user or user in prof.friends.all():
        return render_to_response('profile/albums.html', {'other_user': other_user},
                context_instance=RequestContext(request))

    return HttpResponseRedirect('/')

@login_required
def view_friends(request, url):
    user = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user

    if util.can_users_interract(user, other_user):
        return render_to_response('profile/friends.html', {'other_user': other_user},
                context_instance=RequestContext(request))

@login_required
def create_album(request, url):
    user = request.user
    if request.method == 'POST':
        form = myforms.AlbumForm(request.POST)
        if form.is_valid():
            album = Album.objects.create(name=form.cleaned_data['name'])
            album.save()
            user.get_profile().albums.add(album)
            return HttpResponseRedirect('/profile/'+user.get_profile().url+'/albums')

    form = myforms.AlbumForm()
    return render_to_response('profile/album_new.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def album(request, url, album_id):
    user = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user
    if user == other_user or user in prof.friends.all():
        album = get_object_or_404(Album, id=album_id)
        return render_to_response('profile/album.html', {'album': album, 'other_user': other_user},
                context_instance=RequestContext(request))

    return HttpResponseRedirect('/')

@login_required
def view_img(request, url, img_id):
    prof = UserProfile.objects.get(url=url)
    other_user = prof.user
    user = request.user
    form = myforms.CommentForm()
    if user == other_user or user in other_user.get_profile().friends.all():
        img = Picture.objects.get(id=img_id)
        return render_to_response('profile/view_img.html', {'img': img, 'other_user': other_user, 'form': form},
            context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/dashboard/')

@login_required
def upload_img(request, album_id):
    form = myforms.PictureForm()
    if request.method == 'POST':
        pic = Picture(uploaded=datetime.datetime.now())
        form = myforms.PictureForm(request.POST, request.FILES, instance=pic)
        if form.is_valid():
            album = Album.objects.get(id=album_id)
            pic = form.save()
            album.pictures.add(pic)
            album.save()
            return HttpResponseRedirect('/profile/'+request.user.get_profile().url+'/albums/'+album_id+'/')

    return render_to_response('profile/img_upload.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def delete_img(request, url, img_id):
    user = request.user
    profile = user.get_profile()
    user_imgs = user.get_profile().albums
    img = get_object_or_404(Picture, id=img_id)

    for a in user_imgs.all():
        if img in a.pictures.all():
            if img == profile.profile_picture:
                profile.profile_picture = None
                profile.save()

            a.pictures.remove(img)
            img.delete()
            break

    return HttpResponseRedirect('/profile/'+url+'/albums/'+str(a.id))

@login_required
def comment_img(request, url, img_id):
    user = request.user
    prof = UserProfile.objects.get(url=url)
    other_user = prof.user
    img = get_object_or_404(Picture, id=img_id)
    if util.can_users_interract(user, other_user):
        if request.method == 'POST':
            comment = Comment.objects.create(
                    author=user,
                    read=False,
                    sent = datetime.datetime.now()
                    )
            form = myforms.CommentForm(request.POST, instance=comment)
            comment = form.save()
            img.comments.add(comment)
    return HttpResponseRedirect('/profile/'+url+'/images/'+str(img_id)+'/view/')

@login_required
def set_profile_pic(request, url, img_id):
    user = request.user
    prof = user.get_profile()
    user_imgs = prof.albums
    img = Picture.objects.get(id=img_id)
    for a in user_imgs.all():
        if img in a.pictures.all():
            prof.profile_picture = img
            prof.save()
    return HttpResponseRedirect('/profile/'+prof.url+'/')

@login_required
def invite(request, url):
    sender = request.user
    prof = get_object_or_404(UserProfile, url=url)
    other_user = prof.user

    #check for existing invites
    try:
        inv = prof.invites.get(sender=sender)
    except Invite.DoesNotExist:
        inv = Invite.objects.create(
                sender=sender,
                user=other_user,
                sent=datetime.datetime.now(),
                )
        prof.invites.add(inv)

    #Go back to user's profile
    return HttpResponseRedirect('/profile/'+prof.url+'/')

@login_required
def accept_inv(request, url):
    user = request.user
    prof = UserProfile.objects.get(url=url)
    sender = prof.user

    inv = Invite.objects.get(user=user, sender=sender)
    user.get_profile().friends.add(sender)
    sender.get_profile().friends.add(user)
    inv.delete()
    return HttpResponseRedirect('/dashboard/')

@login_required
def ignore_inv(request, url):
    user = request.user
    prof = User.objects.get(url=url)
    sender = prof.user
    inv = Invite.objects.get(user=user, sender=sender)
    inv.delete()
    return HttpResponseRedirect('/dashboard/')

@login_required
def events(request):
    events = request.user.get_profile().events
    return render_to_response('events/events.html', {'events': events},
            context_instance=RequestContext(request))

@login_required
def create_event(request):
    user = request.user
    form = myforms.EventForm()
    if request.method == 'POST':
        event = Event(author=user)
        form = myforms.EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            event.attending.add(user)
            user.get_profile().events.add(event)
            return HttpResponseRedirect('/events/%d/' % event.id)

    return render_to_response('events/new_event.html', {'form': form},
            context_instance=RequestContext(request))

@login_required
def event_view(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id)

    # Get list of users not invited yet
    invitable = set(user.get_profile().friends.all())
    invitable = invitable.difference(set(event.attending.all()))
    invitable = invitable.difference(set(event.maybe.all()))
    invitable = invitable.difference(set(event.not_attending.all()))
    invitable = invitable.difference(set(event.awaiting.all()))

    if request.method == 'POST':
        to_invite = request.POST.getlist('invites')
        now = datetime.datetime.now()
        for u in to_invite:
            other_user = User.objects.get(id=u)
            inv = EventInvite.objects.create(user=other_user, sent=now, event=event)
            inv.save()
            event.awaiting.add(other_user)
            other_user.get_profile().event_invites.add(inv)

    return render_to_response('events/event.html', {'event': event, 'invitable': invitable},
            context_instance=RequestContext(request))

@login_required
def event_accept(request, event_id):
    user = request.user
    event = Event.objects.get(id=event_id)
    #make sure the user is actually invited
    for i in user.get_profile().event_invites.all():
        if i.event == event:
            event.attending.add(user)
            event.awaiting.remove(user)
            user.get_profile().events.add(event)
            i.delete()

    return HttpResponseRedirect('/dashboard')

@login_required
def event_maybe(request, event_id):
    user = request.user
    event = Event.objects.get(id=event_id)
    #make sure the user is actually invited
    for i in user.get_profile().event_invites.all():
        if i.event == event:
            event.maybe.add(user)
            event.awaiting.remove(user)
            user.get_profile().events.add(event)
            i.delete()

    return HttpResponseRedirect('/dashboard')

@login_required
def event_decline(request, event_id):
    user = request.user
    event = Event.objects.get(id=event_id)
    #make sure the user is actually invited
    for i in user.get_profile().event_invites.all():
        if i.event == event:
            event.not_attending.add(user)
            event.awaiting.remove(user)
            i.delete()

    return HttpResponseRedirect('/dashboard')

@login_required
def search(request):
    form = myforms.SearchForm()
    results = None
    if request.method == 'POST':
        form = myforms.SearchForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            if email:
                results = User.objects.filter(email=email)
            elif name:
                try:
                    name_l = name.split(' ')
                    first_name = name_l[0]
                    last_name = name_l[1]
                except IndexError:
                    first_name = ''
                    last_name = ''
                results = User.objects.filter(first_name__iexact=first_name,
                        last_name__iexact=last_name)

    return render_to_response('search.html', {'form': form, 'results': results},
            context_instance=RequestContext(request))

def philosophy(request):
    return render_to_response('philosophy.html', {},
            context_instance=RequestContext(request))

