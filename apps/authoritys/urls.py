from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[authoritys]'

urlpatterns = [
    path(r'gpu_list/',GpuListView.as_view(), name='gpu_list'),#权限管理列表
    path(r'rolecreate/', RoleCreateView.as_view(), name='rolecreate'),  # 新增角色
    path(r'permissionupdate/', PermissionUpdateView.as_view(), name='permissionupdate'),  # 权限修改
    path(r'roledelete/', RoleDeleteView.as_view(), name='roledelete'),  # 角色删除



]