from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from shade.social import forms as myforms
from shade.social import util
from shade.social.models import UserProfile, Comment, Album, Picture
import datetime, os

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

            if os.path.isfile(img.image.path):
                os.remove(img.image.path)
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

