from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[users]'

urlpatterns = [
    path(r'user_create/',UserCreateView.as_view(), name='user_create'),  #增
    path(r'user_delete/<int:pk>',UserDeleteView.as_view(), name='user_delete'),#删
    path(r'user_list/',UserListView.as_view(), name='user_list'),#查
    path(r'user_update/<int:pk>',UserUpdateView.as_view(), name='user_update'),#改用户信息
    path(r'user_statu_update/<int:pk>', UserStatusUpdateView.as_view(), name='user_statu_update'),  # 改用户状态

]