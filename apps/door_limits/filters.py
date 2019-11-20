from django_filters import rest_framework
from .models import *

#自定义过滤器
class DoorLimitsFilter(rest_framework.FilterSet):
    start_addtime=rest_framework.NumberFilter(field_name='door_addtime',lookup_expr='gte')
    end_addtime  =rest_framework.NumberFilter(field_name='door_addtime',lookup_expr='lte')

    start_audittime=rest_framework.NumberFilter(field_name='door_audittime',lookup_expr='gte')
    end_audittime  =rest_framework.NumberFilter(field_name='door_audittime',lookup_expr='gte')
    class Meta:
        model =Door_approval
        fields = ['door_status','start_addtime','end_addtime','start_audittime','end_audittime']

class DoorStatFilter(rest_framework.FilterSet):
    start_addtime=rest_framework.NumberFilter(field_name='door_addtime',lookup_expr='gte')
    end_addtime  =rest_framework.NumberFilter(field_name='door_addtime',lookup_expr='lte')

    class Meta:
        model =Door_approval
        fields = ['start_addtime','end_addtime']
