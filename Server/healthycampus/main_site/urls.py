from django.conf.urls import patterns, url

from main_site import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView, name='index'),
)