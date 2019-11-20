from django_filters import rest_framework
from .models import *

# #自定义过滤器
# class LogFilter(rest_framework.FilterSet):
#     log_addtime_min=rest_framework.DateTimeFilter(field_name='log_addtime',lookup_expr='gte')
#     log_addtime_max=rest_framework.DateTimeFilter(field_name='log_addtime',lookup_expr='lte')
#
#
#     class Meta:
#         model =Users
#         fields = ['log_addtime_min','log_addtime_max',]

