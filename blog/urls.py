from django.conf.urls import include,url
from . import views
from accounts.views import (login_view, logout_view, register_view)
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^register/$',register_view, name='register'),
    url(r'^login/$',login_view, name='login'),
    url(r'^logout/$',logout_view, name='logout'),
    url(r'^$', views.post_list, name='post_list'),
]