from collections import Counter

from django.db import connection
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view,schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group,Permission
from .models import *
from .serializers import *
from .filters import *
from .schema import AlarmStatisticsSchema,AlarmTypePrecentSchema


# Create your views here.

class AlarmCreateView(generics.CreateAPIView):
    serializer_class = AlarmSerializer

    # 自定义返回结果
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # 失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '添加失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 成功后返回信息的定制
        res = Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        res.data['code'] = 200
        res.data['message'] = "亲，添加成功了"
        return res


class AlarmListView(generics.ListAPIView):
    '''
       1  警告列表
       ---
       ### 参数说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |page|分页|False|int|
       |scene_id|场景id|False|srting|
       |am_type_id|告警类型False|string|
       |am_level_id|告警级别|False|string|
       |am_status|告警状态(1,"待处理"),(2,"待审核"),(3,"审核通过"),(4,"审核未通过")|False|int|
       |start_addtime|告警添加开始时间|False|datetime|
       |end_addtime|告警添加开始结束|False|datetime|
       |ordering|排序 默认id排序|False||

       ### 响应字段说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |id|告警id|--|int|
       |am_addtime|告警添加时间|False|datetime|
       |am_type_id|告警类型信息|False|srting|
       |am_level_id|告警级别信息|False|srting|
       |scene_id|场景id|False|srting|
       |am_device|告警设备|False|srting|
       |am_contene|告警内容|False|srting|
       |am_status|告警状态(1,"待处理"),(2,"待审核"),(3,"审核通过"),(4,"审核未通过")|False|int|
       |am_deal_user|告警处理人|False|srting|
       |am_deal_time|告警处理时间|False|datetime|
       |am_deal_detail|告警处理说明|False|srting|
       |am_audit_user|告警审核人|False|srting|
       |am_audit_time|告警审核时间|False|datetime|
       |am_audit_detail|告警审核说明|False|srting|

       ### 响应消息：
       |Http响应码|原因|响应模型|
       |--|--|--|
       |200|请求成功|返回告警列表信息|
   '''
    module_perms = []
    queryset = alarm_management.objects.all()
    serializer_class = AlarmSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('-alarm_management_id')
    filterset_class = AlarmFilter

class AlarmDealUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    '''
    2  处理
    ---
    ### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警id|Ture|int|
    |am_deal_detail|处理描述|False|string|


    ### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警id|--|int|
    |am_addtime|告警添加时间|False|datetime|
    |am_type_id|告警类型信息|False|srting|
    |am_level_id|告警级别信息|False|srting|
    |scene_id|场景id|False|srting|
    |am_device|告警设备|False|srting|
    |am_contene|告警内容|False|srting|
    |am_status|告警状态(1,"待处理"),(2,"待审核"),(3,"审核通过"),(4,"审核未通过")|False|int|
    |am_deal_user|告警处理人|False|srting|
    |am_deal_time|告警处理时间|False|datetime|
    |am_deal_detail|告警处理说明|False|srting|
    |am_audit_user|告警审核人|False|srting|
    |am_audit_time|告警审核时间|False|datetime|
    |am_audit_detail|告警审核说明|False|srting|

    ### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回告警信息|
    '''
    module_perms = ['alarm_detail',]
    queryset = alarm_management.objects.all()
    serializer_class = AlarmDealUpdateSerializer

    # 数据编辑用post方式
    def post(self, request, *args, **kwargs):
        # print('request:',request)
        # print(kwargs)
        try:
            self.update(request, *args, **kwargs)  # 调用UpdateModelMixin方法
            door_user = self.request.user.id
            f = alarm_management.objects.get(id=kwargs['pk'])
            f.door_user = door_user
            f.save()
        except:
            return Response(data={'code': 400, 'message': '处理失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code': 200, 'message': '处理成功'}, status=status.HTTP_200_OK)

class AlarmStatusUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    '''
    3  审核
    ---
    ### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警id|Ture|int|
    |am_deal_detail|审核描述|False|string|
    |am_status|告警状态(3,"审核通过"),(4,"审核未通过")|False|int|


    ### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警id|--|int|
    |am_addtime|告警添加时间|False|datetime|
    |am_type_id|告警类型信息|False|srting|
    |am_level_id|告警级别信息|False|srting|
    |scene_id|场景id|False|srting|
    |am_device|告警设备|False|srting|
    |am_contene|告警内容|False|srting|
    |am_status|告警状态(1,"待处理"),(2,"待审核"),(3,"审核通过"),(4,"审核未通过")|False|int|
    |am_deal_user|告警处理人|False|srting|
    |am_deal_time|告警处理时间|False|datetime|
    |am_deal_detail|告警处理说明|False|srting|
    |am_audit_user|告警审核人|False|srting|
    |am_audit_time|告警审核时间|False|datetime|
    |am_audit_detail|告警审核说明|False|srting|

    ### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回告警信息|
    '''
    module_perms = ['alarm_audit', ]
    queryset = alarm_management.objects.all()
    serializer_class = AlarmStatusUpdateSerializer

    # 数据编辑用post方式
    def post(self, request, *args, **kwargs):
        # print('request:',request)
        # print(kwargs)
        try:
            self.update(request, *args, **kwargs)  # 调用UpdateModelMixin方法
            door_user = self.request.user.id
            f = alarm_management.objects.get(id=kwargs['pk'])
            f.door_user = door_user
            f.save()
        except:
            return Response(data={'code': 400, 'message': '审核失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code': 200, 'message': '审核成功'}, status=status.HTTP_200_OK)

class SceneAppertainView(generics.ListAPIView):
    '''
        1.1 所属场景信息
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|--|int|
        |scene_name|场景名称|--|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回所属场景信息|
        '''
    module_perms=[]
    queryset = alarm_management.objects.all()
    serializer_class =AlarmSceneSerializer

class AlarmTypeInfoView(generics.ListAPIView):
    '''
        1.2 告警类型信息
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|告警类型id|--|int|
        |alarm_type_name|告警类型名称|Ture|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回告警类型信息|
        '''
    module_perms = []
    queryset = alarm_management.objects.all()
    serializer_class =AlarmTypeInfoSerializer

class AlarmLeveInfoView(generics.ListAPIView):
    '''
        1.3 告警级别信息
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|告警级别id|--|int|
        |alarm_level_name|告警级别名称|Ture|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回告警级别信息|
        '''
    module_perms = []
    queryset = alarm_management.objects.all()
    serializer_class =AlarmLeveInfoSerializer

class AlarmStatusInfoView(generics.ListAPIView):
    '''
        1.4 告警状态信息
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |am_status|告警状态(1,"待处理"),(2,"待审核"),(3,"审核通过"),(4,"审核未通过")|Ture|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回告警状态信息|
        '''
    module_perms = []
    queryset = alarm_management.objects.all()
    serializer_class =AlarmStatusInfoSerializer

class AlarmTypeNumView(generics.GenericAPIView):
    '''
     4  统计各类型报警占比
     ---
     ### 参数说明
     |字段名称|描述|必须|类型|
     |--|--|--|--|
     |start_addtime|告警添加开始时间|False|datetime|
     |end_addtime|告警添加开始结束|False|datetime|

     ### 响应字段说明
     |字段名称|描述|必须|类型|
     |--|--|--|--|
     | |占比|--|int|

     ### 响应消息：
     |Http响应码|原因|响应模型|
     |--|--|--|
     |200|请求成功|返回占比信息|
     '''
    module_perms = []
    queryset = alarm_management.objects.all()
    serializers =AlarmSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = AlarmStatFilter

    def get(self, request,*args, **kwargs):
        queryset = alarm_management.objects.all()
        am_type_ids=[]
        count=0
        for i in queryset:
            am_type_ids.append(i.am_type_id.alarm_type_name)
            count+=1
        am_type_ids = set(am_type_ids)
        am_type_ids = list(am_type_ids)
        usernums = []
        for user in am_type_ids:
            usernums.append(round(am_type_ids.count(user) /count , 4) * 100)

        pronums = []
        typeids = []
        for i in am_type_ids:
            typeids.append(str(i))
        for j in usernums:
            j = str(j) + "%"
            pronums.append(j)
        doordict = dict(zip(typeids, pronums))

        return Response(doordict)

class AlarmTypeNumView1(APIView):
    module_perms = []
    schema = AlarmStatisticsSchema
    def get(self,request,start_addtime,end_addtime):
        cursor = connection.cursor()
        sql = "select * from alarm_management " \
              "where am_addtime>'{0}'and am_addtime<'{1}' group by scene_id"\
            .format(start_addtime,end_addtime)
        cursor.execute(sql)
        rels = cursor.fetchall()
        print(rels)  # ( (1,'id','email'),(2,'id','email'),) =>转换为[{id:1,s:v,},{ },{}]

        cursor.close()
        return


class AlarmStatusNumView(generics.GenericAPIView):
    '''
        5 统计安监测告警各状态数量占比
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |start_addtime|告警添加时间|False|datetime|
        |start_addtime|告警添加时间|False|datetime|
        |am_type_id|告警类型id|False|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        ||占比信息|--|dict|


        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回占比信息|
        '''
    module_perms = []
    queryset = alarm_management.objects.all()
    serializers =AlarmSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AlarmStatusFilter

    def get(self, request, *args, **kwargs):
        queryset = alarm_management.objects.all()
        am_status = []
        count = 0
        for i in queryset:
            am_status.append(i.am_status)
            count += 1
        am_status = set(am_status)
        am_status = list(am_status)
        statusnums = []
        for user in am_status:
            statusnums.append(round(am_status.count(user) / count, 4) * 100)

        pronums = []
        typeids = []
        for i in am_status:
            typeids.append(str(i))
        for j in statusnums:
            j = str(j) + "%"
            pronums.append(j)
        doordict = dict(zip(typeids, pronums))

        return Response(doordict)

class AlarmNoDealNumView(APIView):
    '''
       6 统计某时刻所有未处理告警时间和
       ---
       ### 参数说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |page|分页|True|int|
       |start_addtime|告警添加时间|False|datetime|
       |start_addtime|告警添加时间|False|datetime|

       ### 响应字段说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       ||占比信息|--|dict|

       ### 响应消息：
       |Http响应码|原因|响应模型|
       |--|--|--|
       |200|请求成功|返回占比信息|
       '''
    module_perms = []
    schema = AlarmTypePrecentSchema

    def post(self, request):
        start_time = self.request.query_params.get('stat_addtime', '')
        end_time = self.request.query_params.get('end_addtime', '')
        if not start_time:
            start_time = '1970-01-01 00:00:00'
        if not end_time:
            end_time = datetime.now()
        queryset = alarm_management.objects.filter(am_addtime__range=(start_time, end_time), am_status=1)
        return Response(data={'code': 200, 'sum_time': calculate_time(queryset)}, status=status.HTTP_200_OK)

# 定义函数，未处理告警时间和计算函数
def calculate_time(queryset):
    alarm_time = []
    for time in queryset:
        alarm_time.append(time.am_addtime)
    result = {}
    print(Counter(alarm_time))
    for key, value in Counter(alarm_time).items():
        result[key.strftime('%Y-%m-%d %H:%M:%S')] = round(((datetime.now() - key).total_seconds() * value) / 60, 0)
    return result


