from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[logs]'

urlpatterns = [
    path(r'loglist/',LogListView.as_view(), name='loglist'),#查
    path(r'log_createExcel/',LogsExcelFile.as_view(), name='log_createExcel'),#导出Excel文件

    path(r'scenes/',SceneAppertainView.as_view(), name='scenes'),#所属场景
    path(r'module/',ModuleAppertainView.as_view(), name='module'),#日志类型
]