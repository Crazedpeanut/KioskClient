from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'healthycampus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('main_site.urls', namespace="main_site")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main_site.urls', namespace="main_site")),
    url(r'^kiosk/', include('kiosk.urls', namespace="kiosk")),
)
