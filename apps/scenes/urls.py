from django.conf.urls import url
from django.urls import path
from .views import *

app_name = '[scenes]'

urlpatterns = [
    path(r'scenecreate/',SceneCreateView.as_view(), name='scenecreate'),  #增
    path(r'scenedelete/<int:pk>',SceneDeleteView.as_view(), name='scenedelete'),#删
    path(r'sceneupdate/<int:pk>',SceneUpdateView.as_view(), name='sceneupdate'),#改
    path(r'scenelist/',SceneListView.as_view(), name='scenelist'),#查

    path(r'scenebrowse/',SceneBrowseView.as_view(), name='scenebrowse'),#5场景浏览信息
    path(r'equipmentstatus/',EquipmentStautsView.as_view(), name='equipmentstatus'),#6查看设备状态

    path(r'scenefirehistory/', SceneFireHistoryView.as_view(), name='scenefirehistory'),  # 7场景消防设备数据统计图
    path(r'scenefirealarm/', SceneFireAlarmView.as_view(), name='scenefirealarm'),  # 8场景消防设备报警统计表
    path(r'sceneenvironmenthistory/', SceneEnvironmentHistoryView.as_view(), name='sceneenvironmenthistory'),# 11场景环境设备数据统计图
    path(r'sceneenvironmentalarm/', SceneEnvironmentAlarmView.as_view(), name='sceneenvironmentalarm'),  # 12场景环境设备报警统计表

    path(r'scenedisplaycreate/', SceneDisplayCreateView.as_view(), name='scenedisplaycreate'),  # 13显示器内容
    path(r'sceneequipmenthistory/', SceneEquipmentHistoryView.as_view(), name='sceneequipmenthistory'),  # 14场景实时设备数据统计图
    path(r'sceneequipmentopen/', SceneEquipmentOpenView.as_view(), name='sceneequipmentopen'),  # 15场景实时设备打开占比图
    path(r'sceneunlocking/', SceneUnlockingView.as_view(), name='sceneunlocking'),  # 16场景开锁记录


]