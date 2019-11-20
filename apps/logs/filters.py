from django_filters import rest_framework
from .models import Logs

#自定义过滤器
class LogFilter(rest_framework.FilterSet):
    log_addtime_min=rest_framework.DateTimeFilter(field_name='log_addtime',lookup_expr='gte')
    log_addtime_max=rest_framework.DateTimeFilter(field_name='log_addtime',lookup_expr='lte')


    class Meta:
        model =Logs
        fields = ['log_addtime_min','log_addtime_max','scene_id','log_module']

