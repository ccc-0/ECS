from django_filters import rest_framework
from .models import *

#自定义过滤器
class SceneFilter(rest_framework.FilterSet):
    scene_addtime_min=rest_framework.DateTimeFilter(field_name='scene_addtime',lookup_expr='gte')
    scene_addtime_max=rest_framework.DateTimeFilter(field_name='scene_addtime',lookup_expr='lte')

    class Meta:
        model =Scene
        fields = ['scene_addtime_min','scene_addtime_max',]

class HumidityFilter(rest_framework.FilterSet):
    humidity_addtime_min=rest_framework.DateTimeFilter(field_name='humidity_insert_time',lookup_expr='gte')
    humidity_addtime_max=rest_framework.DateTimeFilter(field_name='humidity_insert_time',lookup_expr='lte')

    class Meta:
        model =Humidity
        fields = ['humidity_addtime_min','humidity_addtime_min',]

