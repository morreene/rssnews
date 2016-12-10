from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
	url(r'^$', views.articles_list, name='articles_list'),
	url(r'^feeds/new', views.new_feed, name='feed_new'),
	url(r'^feeds/', views.feeds_list, name='feeds_list'),
	
	url(r'^admin/', admin.site.urls),
]
