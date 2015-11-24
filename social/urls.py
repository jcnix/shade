from django.conf.urls import include, url
from django.conf import settings
import views, images, comments, messaging, auth

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/', auth.login, name='login'),
	url(r'^logout/', auth.logout, name='logout'),
	url(r'^register/', auth.register, name='register'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^profile/(?P<url>\w+)/$', views.profile, name='profile'),
	url(r'^profile/(?P<url>\w+)/albums/$', images.albums, name='albums'),
	url(r'^profile/(?P<url>\w+)/comment/$', comments.post, name='post_comment'),
	url(r'^settings/friends/$', views.manage_friends, name='manage_friends'),
	url(r'^settings/password/$', views.change_pass, name='change_pass'),
	url(r'^inbox/$', messaging.inbox, name='inbox'),
	url(r'^events/$', views.events, name='events'),
	url(r'^search/$', views.search, name='search'),
	url(r'^settings/friends/(?P<id>\d+)/$', views.manage_friend, name='manage_friend'),
	url(r'^settings/friends/group/new/$', views.new_group, name='new_group'),
	url(r'^settings/friends/group/(?P<id>\d+)/new/$', views.new_group),
	url(r'^settings/friends/group/(?P<id>\d+)/edit/$', views.edit_group, name='edit_group'),
	url(r'^settings/friends/group/set_order/$', views.sort_group, name='sort_group'),
	url(r'^profile/(?P<url>\w+)/subscribe/$', views.subscribe, name='subscribe'),
	url(r'^profile/(?P<url>\w+)/comment/(?P<comment_id>\d+)/reply/$', comments.reply, name='comment_reply'),
	url(r'^profile/(?P<url>\w+)/comment/(?P<comment_id>\d+)/delete/$', comments.delete, name='comment_delete'),
	url(r'^profile/(?P<url>\w+)/friends/$', views.view_friends, name='view_friends'),
	url(r'^profile/(?P<url>\w+)/albums/create/$', images.create_album, name='create_album'),
	url(r'^profile/(?P<url>\w+)/albums/(?P<album_id>\d+)/$', images.album, name='album'),
	url(r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/view/$', images.view_img, name='view_img'),
	url(r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/delete/$', images.delete_img, name='delete_img'),
	url(r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/comment/$', images.comment_img, name='comment_img'),
	url(r'^profile/albums/(?P<album_id>\d+)/upload/$', images.upload_img, name='upload_img'),
	url(r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/set_profile_pic$', images.set_profile_pic, name='set_profile_pic'),
	url(r'^invite/(?P<url>\w+)/$', views.invite, name='invite'),
	url(r'^invite/accept/(?P<url>\w+)/$', views.accept_inv, name='accept_inv'),
	url(r'^invite/ignore/(?P<url>\w+)/$', views.ignore_inv, name='ignore_inv'),
	url(r'^inbox/view/(?P<msg_id>\d+)/$', messaging.msg_view, name='msg_view'),
	url(r'^inbox/compose/$', messaging.msg_compose, name='msg_compose'),
	url(r'^inbox/reply/(?P<msg_id>\d+)/$', messaging.msg_compose, name='msg_reply'),
	url(r'^inbox/delete/(?P<msg_id>\d+)/$', messaging.msg_delete, name='msg_delete'),
	url(r'^events/new/$', views.create_event, name='create_event'),
	url(r'^events/(?P<event_id>\d+)/$', views.event_view, name='event_view'),
	url(r'^events/(?P<event_id>\d+)/accept/$', views.event_accept, name='event_accept'),
	url(r'^events/(?P<event_id>\d+)/possible/$', views.event_maybe, name='event_maybe'),
	url(r'^events/(?P<event_id>\d+)/decline/$', views.event_decline, name='event_decline'),
	url(r'^philosophy/$', views.philosophy, name='philosophy'),
]

if settings.DEBUG:
	urlpatterns += url(r'^shade/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),


