from django.conf.urls.defaults import *
from django.conf import settings
import socialauth

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'shade.social.views.index'),
    (r'^dashboard/$', 'shade.social.views.dashboard'),
    (r'^settings/$', 'shade.social.views.settings'),
    (r'^profile/(?P<url>\w+)/$', 'shade.social.views.profile'),
    (r'^profile/(?P<url>\w+)/albums/$', 'shade.social.views.albums'),
    (r'^profile/(?P<url>\w+)/albums/create/$', 'shade.social.views.create_album'),
    (r'^profile/(?P<url>\w+)/albums/(?P<album_id>\d+)/$', 'shade.social.views.album'),
    (r'^profile/(?P<url>\w+)/view_image/(?P<img_id>\d+)/$', 'shade.social.views.view_img'),
    (r'^profile/albums/(?P<album_id>\d+)/upload/$', 'shade.social.views.upload_img'),
    (r'^profile/set_profile_pic/(?P<img_id>\d+)/$', 'shade.social.views.set_profile_pic'),
    (r'^invite/(?P<url>\w+)/$', 'shade.social.views.invite'),
    (r'^invite/accept/(?P<url>\w+)/$', 'shade.social.views.accept_inv'),
    (r'^invite/ignore/(?P<url>\w+)/$', 'shade.social.views.ignore_inv'),
    (r'^inbox/$', 'shade.social.views.inbox'),
    (r'^inbox/view/(?P<msg_id>\d+)/$', 'shade.social.views.msg_view'),
    (r'^inbox/compose/$', 'shade.social.views.msg_compose'),
    (r'^inbox/reply/(?P<msg_id>\d+)/$', 'shade.social.views.msg_compose'),
    (r'^events/$', 'shade.social.views.events'),
    (r'^events/new/$', 'shade.social.views.create_event'),
    (r'^events/(?P<event_id>\d+)/$', 'shade.social.views.event_view'),
    (r'^search/$', 'shade.social.views.search'),
    (r'^philosophy/$', 'shade.social.views.philosophy'),

    # OpenID
    (r'^login/', 'shade.social.views.index'),
    (r'^accounts/', include('socialauth.urls')),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/shade/favicon.ico'}),
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^shade/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

