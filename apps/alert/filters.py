from django_filters import rest_framework
from .models import *


class AlarmFilter(rest_framework.FilterSet):
    start_addtime=rest_framework.NumberFilter(field_name='am_addtime',lookup_expr='gte')
    end_addtime  =rest_framework.NumberFilter(field_name='am_addtime',lookup_expr='lte')

    class Meta:
        model =alarm_management
        fields = ['scene_id','am_type_id','am_level_id','am_status','start_addtime','end_addtime']

class AlarmStatFilter(rest_framework.FilterSet):
    start_addtime=rest_framework.NumberFilter(field_name='am_addtime',lookup_expr='gte')
    end_addtime  =rest_framework.NumberFilter(field_name='am_addtime',lookup_expr='lte')

    class Meta:
        model =alarm_management
        fields = ['start_addtime','end_addtime']

class AlarmStatusFilter(rest_framework.FilterSet):
    start_addtime=rest_framework.NumberFilter(field_name='am_addtime',lookup_expr='gte')
    end_addtime  =rest_framework.NumberFilter(field_name='am_addtime',lookup_expr='lte')

    class Meta:
        model =alarm_management
        fields = ['start_addtime','end_addtime','am_type_id']
