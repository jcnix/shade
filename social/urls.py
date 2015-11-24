from django.conf.urls import include, url
from django.conf import settings
import views, auth

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login/', auth.login),
	url(r'^logout/', auth.logout),
	url(r'^register/', auth.register),
	url(r'^dashboard/$', views.dashboard),
	url(r'^settings/$', views.settings),
	url(r'^settings/friends/$', views.manage_friends),
]

if settings.DEBUG:
	urlpatterns += url(r'^shade/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),


