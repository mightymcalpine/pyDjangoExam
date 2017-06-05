from . import views
from django.conf.urls import url

urlpatterns = [
	url(r'^home$', views.home, name="home"),
	url(r'^newTrip$', views.newTrip, name="newTrip"),
	url(r'^addTrip$', views.addTrip, name="addTrip"),
	url(r'^tripProfile/(?P<id>\d+)$', views.tripProfile, name="tripProfile"),
	url(r'^join/(?P<id>\d+)$',views.join, name="join" ),
]