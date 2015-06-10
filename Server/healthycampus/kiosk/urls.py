from django.conf.urls import patterns, url

from kiosk import views

urlpatterns = patterns('',
	url(r'^$', views.kiosk, name='kiosk'),
    url(r'^leaderboards/$', views.global_leaderboards, name='leaderboards'),
    url(r'^user_checkin/$', views.user_checkin, name='user_checkin'),
    url(r'^user_checkin_file/$', views.user_checkin_file, name='user_checkin_file'),
    url(r'^heartbeat_checkin/$', views.heartbeat_checkin, name='heartbeat_checkin'),
    url(r'^user/$', views.user_detail_search, name='user_detail_search'),
    url(r'^user/(?P<user_id>\S+)/$', views.user_detail, name='user_detail'),
    url(r'checkin/test/$', views.test, name='test_form'),
)