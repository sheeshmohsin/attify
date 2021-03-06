from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'android.views.home', name='home'),
    url(r'^details/$', 'android.views.details', name='details'),
    url(r'^dirstructure/$', 'android.views.dirlist', name='dirlist'),
    url(r'^filecontent/$', 'android.views.filecontent', name='getContent'),
    url(r'^setcontent/$', 'android.views.setcontent', name='setContent'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
