from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'shade.social.views.index'),
    (r'^login/', 'shade.social.auth.login'),
    (r'^logout/', 'shade.social.auth.logout'),
    (r'^register/', 'shade.social.auth.register'),
    (r'^dashboard/$', 'shade.social.views.dashboard'),
    (r'^settings/$', 'shade.social.views.settings'),
    (r'^settings/friends/$', 'shade.social.views.manage_friends'),
    (r'^settings/friends/(?P<id>\d+)/$', 'shade.social.views.manage_friend'),
    (r'^settings/friends/group/new/$', 'shade.social.views.new_group'),
    (r'^settings/friends/group/(?P<id>\d+)/new/$', 'shade.social.views.new_group'),
    (r'^settings/friends/group/(?P<id>\d+)/edit/$', 'shade.social.views.edit_group'),
    (r'^settings/friends/group/set_order/$', 'shade.social.views.sort_group'),
    (r'^settings/password/$', 'shade.social.views.change_pass'),
    (r'^profile/(?P<url>\w+)/$', 'shade.social.views.profile'),
    (r'^profile/(?P<url>\w+)/subscribe/$', 'shade.social.views.subscribe'),
    (r'^profile/(?P<url>\w+)/comment/$', 'shade.social.comments.post'),
    (r'^profile/(?P<url>\w+)/comment/(?P<comment_id>\d+)/reply/$', 'shade.social.comments.reply'),
    (r'^profile/(?P<url>\w+)/comment/(?P<comment_id>\d+)/delete/$', 'shade.social.comments.delete'),
    (r'^profile/(?P<url>\w+)/friends/$', 'shade.social.views.view_friends'),
    (r'^profile/(?P<url>\w+)/albums/$', 'shade.social.images.albums'),
    (r'^profile/(?P<url>\w+)/albums/create/$', 'shade.social.images.create_album'),
    (r'^profile/(?P<url>\w+)/albums/(?P<album_id>\d+)/$', 'shade.social.images.album'),
    (r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/view/$', 'shade.social.images.view_img'),
    (r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/delete/$', 'shade.social.images.delete_img'),
    (r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/comment/$', 'shade.social.images.comment_img'),
    (r'^profile/albums/(?P<album_id>\d+)/upload/$', 'shade.social.images.upload_img'),
    (r'^profile/(?P<url>\w+)/images/(?P<img_id>\d+)/set_profile_pic$', 'shade.social.images.set_profile_pic'),
    (r'^invite/(?P<url>\w+)/$', 'shade.social.views.invite'),
    (r'^invite/accept/(?P<url>\w+)/$', 'shade.social.views.accept_inv'),
    (r'^invite/ignore/(?P<url>\w+)/$', 'shade.social.views.ignore_inv'),
    (r'^inbox/$', 'shade.social.messaging.inbox'),
    (r'^inbox/view/(?P<msg_id>\d+)/$', 'shade.social.messaging.msg_view'),
    (r'^inbox/compose/$', 'shade.social.messaging.msg_compose'),
    (r'^inbox/reply/(?P<msg_id>\d+)/$', 'shade.social.messaging.msg_compose'),
    (r'^inbox/delete/(?P<msg_id>\d+)/$', 'shade.social.messaging.msg_delete'),
    (r'^events/$', 'shade.social.views.events'),
    (r'^events/new/$', 'shade.social.views.create_event'),
    (r'^events/(?P<event_id>\d+)/$', 'shade.social.views.event_view'),
    (r'^events/(?P<event_id>\d+)/accept/$', 'shade.social.views.event_accept'),
    (r'^events/(?P<event_id>\d+)/possible/$', 'shade.social.views.event_maybe'),
    (r'^events/(?P<event_id>\d+)/decline/$', 'shade.social.views.event_decline'),
    (r'^search/$', 'shade.social.views.search'),
    (r'^philosophy/$', 'shade.social.views.philosophy'),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/shade/favicon.ico'}),
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^shade/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

