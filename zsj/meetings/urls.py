from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^createMtn/$', views.createMtn, name='createMtn'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<meeting_id>\d+)/vote/$', views.vote, name='vote'),
    # organizer_name
    url(r'^(?P<pk>\d+)/nameMtn/$', views.NameView.as_view(), name='nameMtn'),
    url(r'^(?P<meeting_id>\d+)/name/$', views.name, name='name'),	
    # organizer_availability
    url(r'^(?P<meeting_id>\d+)/availability_organizer/$', views.availability_organizer, name='availability_organizer'),
    url(r'^(?P<meeting_id>\d+)/availability_organizer_handler/$', views.availability_organizer_handler, name='availability_organizer_handler'),
    # share
    url(r'^(?P<pk>\d+)/share/$', views.ShareView.as_view(), name='share'),

    # availability_general
    url(r'^(?P<meeting_id>\d+)/availability/$', views.Availability, name='availability'),
    url(r'^(?P<meeting_id>\d+)/availability_general_handler/$', views.availability_general_handler, name='availability_general_handler'),

    # result
    url(r'^result/$', views.result, name='result'),

	)	