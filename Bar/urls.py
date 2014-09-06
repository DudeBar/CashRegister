from django.conf.urls import patterns, url

from Bar import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^open$', views.open, name='open'),
    url(r'^close$', views.close, name='close'),
    url(r'^make_command/(?P<barman_id>\d+)/$', views.make_command, name='make_command'),
    )