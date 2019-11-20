from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[video]'

urlpatterns = [
    path(r'addvideo/',AddVideoView.as_view(), name='videocreate'),  #增
    path(r'videodelete/<int:pk>',VideoDeleteView.as_view(), name='videodelete'),#删
    path(r'videoupdate/<int:pk>',VideoUpdateView.as_view(), name='videoupdate'),#改
    path(r'videolist/',VideoListView.as_view(), name='videolist'),#查

]