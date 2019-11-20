from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[alarms]'

urlpatterns = [
    path(r'alarms_dealupdate/<int:pk>',AlarmDealUpdateView.as_view(), name='alarms_dealupdate'),#处理
    path(r'alarms_statusupdate/<int:pk>',AlarmStatusUpdateView.as_view(), name='alarms_statusupdate'),#审核
    path(r'alarms_list/',AlarmListView.as_view(), name='alarms_list'),# 查
    path(r'alarms_scene/',SceneAppertainView.as_view(), name='alarms_scene'),# 所属场景信息
    path(r'alarms_type/',AlarmTypeInfoView.as_view(), name='alarms_type'),# 告警类型信息
    path(r'alarms_leve/',AlarmLeveInfoView.as_view(), name='alarms_leve'),# 告警级别信息
    path(r'alarms_status/', AlarmStatusInfoView.as_view(), name='alarms_status'),  # 告警状态信息

    # url(r'^alarmstypenum/((?P<year>\d{4})(?P<month>\d{2})/)', AlarmTypeNumView.as_view(), name='alarmstypenum'),
    path(r'alarmstypenum/', AlarmTypeNumView.as_view(), name='alarmstypenum'),  # 统计各类型报警
    path(r'alarmsstatusnum/', AlarmStatusNumView.as_view(), name='alarmsstatusnum'),  # 统计安监测告警各状态数量占比
    path(r'alarmsnodealnum/', AlarmNoDealNumView.as_view(), name='alarmsnodealnum'),  # 统计某时刻所有未处理告警时间和

]