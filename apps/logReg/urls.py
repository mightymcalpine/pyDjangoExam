from . import views
from django.conf.urls import url

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^register$', views.process, name="register"),
	url(r'^login$', views.process, name="login"),
	url(r'^logout$', views.logout, name="logout")
] 

