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
]

if settings.DEBUG:
	urlpatterns += url(r'^shade/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),


