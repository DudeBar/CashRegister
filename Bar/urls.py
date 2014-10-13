from django.conf.urls import patterns, url

from Bar import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^open$', views.open, name='open'),
    url(r'^close$', views.close, name='close'),
    url(r'^make_command/(?P<barman_id>\d+)/$', views.make_command, name='make_command'),
    url(r'^add_command/$', views.add_command, name='add_command'),
    url(r'^category_onclick/(?P<category_id>\d+)/$', views.category_onclick, name='category_onclick'),
    url(r'^product_onclick/(?P<product_id>\d+)/$', views.product_onclick, name='product_onclick'),
    url(r'^set_happy_hour/$', views.set_happy_hour, name='set_happy_hour'),
    url(r'^get_solde/$', views.get_solde, name='get_solde'),
    url(r'^add_note/$', views.add_note, name='add_note'),
    url(r'^del_note/$', views.del_note, name='del_note'),
    )