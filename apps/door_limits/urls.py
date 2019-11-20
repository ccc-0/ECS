from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[door_limits]'

urlpatterns = [
    path(r'door_limits_create/',DoorLimitsCreateView.as_view(), name='door_limits_create'),  #增
    path(r'door_limits_update/<int:pk>',DoorLimitsUpdateView.as_view(), name='door_limits_update'),#改
    path(r'door_limits_list/',DoorLimitsListView.as_view(), name='door_limits_list'),#查
    path(r'doorstatusinfo/',DoorStatusInfoView.as_view(), name='doorstatusinfo'),#申请状态
    path(r'door_limits_Excel/', DoorExcelFile.as_view(), name='door_limits_Excel'),#导出

    path(r'doorstatnum/',DoorStatNumView.as_view(), name='doorstatnum'),#统计开门次数
    path(r'doorstattime/',DoorStatTimeView.as_view(), name='doorstattime'),#统计开门时间

]