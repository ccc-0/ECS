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
import xlwt
from io import BytesIO
from  .models import *
from  .serializers import *
from  .filters import *

# Create your views here.
class DoorLimitsListView(generics.ListAPIView):
    '''
       1 门禁列表
       ---
       ### 参数说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |page|分页|False|int|
       |door_status|门禁申请状态(1,'待审核'),(2,'已通过'),(3,'已拒绝')|False|int|
       |start_addtime|申请添加开始时间|False|datetime|
       |end_addtime|申请添加结束时间|False|datetime|
       |start_audittime|审批开始时间|False|datetime|
       |end_audittime|审批结束时间|False|datetime|
       |ordering|以哪个字段排序，默认id|False|string|

       ### 响应字段说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |id|视频id|--|int|
       |door_addtime|门禁申请时间|False|datatime|
       |door_start|申请开始时间|False|datatime|
       |door_end|申请结束时间|False|datatime|
       |door_follow|随行人员|False|string|
       |door_follownum|随行人数|False|int|
       |door_detail|申请说明|False|string|
       |door_status|申请状态(1,'待审核'),(2,'已通过'),(3,'已拒绝')|False|int|
       |door_user|审核人|False|string|
       |door_audittime|审批时间|False|datatime|
       |door_feedback|审批反馈|False|string|
       |user_id|申请用户id|Ture|int|
       |scene_id|所属模块|False|int|

       ### 响应消息：
       |Http响应码|原因|响应模型|
       |--|--|--|
       |200|请求成功|返回视频信息|
   '''
    module_perms = ['door_limits.door_view']
    queryset = Door_approval.objects.all()  # 查询结果集设置
    serializer_class = DoorLimitsSerializer  # 序列化器设置

    # 过滤器使用
    # (DjangoFilterBackend过滤,SearchFilter搜索,OrderingFilter排序）
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('-door_id')
    # 使用自定义过滤器
    filterset_class = DoorLimitsFilter


class DoorLimitsCreateView(generics.CreateAPIView):
    '''
       2 创建申请
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |door_start|申请开始时间|False|datatime|
       |door_end|申请结束时间|False|datatime|
       |door_follow|随行人员|False|string|
       |door_follownum|随行人数|False|int|
       |door_detail|申请说明|False|string|
       |scene_id|所属模块|False|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |字段名称|描述|必须|类型|
       |--|--|--|--|
       |id|视频id|--|int|
       |door_addtime|门禁申请时间|False|datatime|
       |door_start|申请开始时间|False|datatime|
       |door_end|申请结束时间|False|datatime|
       |door_follow|随行人员|False|string|
       |door_follownum|随行人数|False|int|
       |door_detail|申请说明|False|string|
       |door_status|申请状态(1,'待审核'),(2,'已通过'),(3,'已拒绝')|False|int|
       |door_user|审核人|False|string|
       |door_audittime|审批时间|False|datatime|
       |door_feedback|审批反馈|False|string|
       |user_id|申请用户id|Ture|int|
       |scene_id|所属模块|False|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |201|添加成功|返回视频信息|
    '''
    module_perms = ['door_limits.door_audit']
    serializer_class = DoorLimitsCreateSerializer
    # 自定义返回结果
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # 失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '申请失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 成功后返回信息的定制
        res = Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        res.data['code'] = 200
        res.data['message'] = "亲，申请成功了"
        return res


class DoorLimitsUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    '''
        3 审批
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|视频id|Ture|int|
        |door_feedback|审批反馈|False|string|
        |door_status|申请状态(1,'待审核'),(2,'已通过'),(3,'已拒绝')|False|int|

        ### 响应字段说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |id|视频id|--|int|
       |door_addtime|门禁申请时间|False|datatime|
       |door_start|申请开始时间|False|datatime|
       |door_end|申请结束时间|False|datatime|
       |door_follow|随行人员|False|string|
       |door_follownum|随行人数|False|int|
       |door_detail|申请说明|False|string|
       |door_status|申请状态(1,'待审核'),(2,'已通过'),(3,'已拒绝')|False|int|
       |door_user|审核人|False|string|
       |door_audittime|审批时间|False|datatime|
       |door_feedback|审批反馈|False|string|
       |user_id|申请用户id|Ture|int|
       |scene_id|所属模块|False|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回门禁信息|
    '''
    module_perms = ['door_limits.door_audit']
    queryset = Door_approval.objects.all()
    serializer_class = DoorLimitsUpdateSerializer

    # 数据编辑用post方式
    def post(self, request, *args, **kwargs):
        # print('request:',request)
        # print(kwargs)
        try:
            self.update(request, *args, **kwargs)  # 调用UpdateModelMixin方法
            door_user = self.request.user.id
            f = Door_approval.objects.get(id=kwargs['pk'])
            f.door_user = door_user
            f.save()
        except:
            return Response(data={'code': 400, 'message': '审批失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code': 200, 'message': '审批成功'}, status=status.HTTP_200_OK)


class DoorExcelFile(APIView):
    '''
        7 导出
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        ### 响应字段说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回下载文件|
    '''
    module_perms = ['door_limits.door_view']
    permission_classes = ()
    filter_backends = (DjangoFilterBackend,)
    # 使用自定义过滤器
    filterset_class = DoorStatFilter

    def get(self, request):
        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=DoorLimits.xls'  # 文件名称
        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('DoorLimits-sheet')

        # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
        style_heading = xlwt.easyxf("""
                    font:
                        name Arial,
                        colour_index white,
                        bold on,
                        height 0xA0;
                    align:
                        wrap off,
                        vert center,
                        horiz center;
                    pattern:
                        pattern solid,
                        fore-colour 0x19;
                    borders:
                        left THIN,
                        right THIN,
                        top THIN,
                        bottom THIN;
                    """)

        # 写入文件标题
        sheet.write(0, 0, '序号', style_heading)
        sheet.write(0, 1, '申请人', style_heading)
        sheet.write(0, 2, '申请时间', style_heading)
        sheet.write(0, 3, '申请说明', style_heading)
        sheet.write(0, 4, '随行人数', style_heading)
        sheet.write(0, 5, '随行人员', style_heading)
        sheet.write(0, 6, '申请状态', style_heading)
        sheet.write(0, 7, '审批时间', style_heading)
        sheet.write(0, 8, '审批人', style_heading)
        sheet.write(0, 9, '审批反馈', style_heading)

        # 写入数据
        data_row = 1
        # User.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in Door_approval.objects.all():
            # 格式化datetime
            door_addtime = i.door_addtime.strftime('%Y-%m-%d')
            if i.door_audittime:
                door_audittime= i.door_audittime.strftime('%Y-%m-%d')
            else:
                door_audittime=None
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.user_id.last_name)
            sheet.write(data_row, 2, door_addtime)
            sheet.write(data_row, 3, i.door_detail)
            sheet.write(data_row, 4, i.door_follownum)
            sheet.write(data_row, 5, i.door_follow)
            sheet.write(data_row, 6, i.door_status)
            sheet.write(data_row, 7, door_audittime)
            sheet.write(data_row, 8, i.door_user)
            sheet.write(data_row, 9, i.door_feedback)
            data_row = data_row + 1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response

class DoorStatNumView(generics.GenericAPIView):
    '''
        4 门禁申请统计
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|False|int|
        |start_addtime|申请添加开始时间|False|datetime|
        |end_addtime|申请添加结束时间|False|datetime|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |申请人用户id|所占百分比|Ture|float|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回门禁统计信息|
    '''
    module_perms = ['door_limits.door_view']
    queryset = Door_approval.objects.all()
    serializers =DoorStatSerialzer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DoorStatFilter

    def get(self, request,*args, **kwargs):
        queryset = Door_approval.objects.filter(door_status=1)
        usersids=[]
        count=0
        for i in queryset:
            usersids.append(i.user_id.last_name)
            count+=1
        # counter
        user_ids=set(usersids)
        user_ids=list(user_ids)
        usernums = []
        for user in user_ids:
            usernums.append(round(usersids.count(user) / count, 4) * 100)

        pronums=[]
        usersid=[]
        for i in user_ids:
            usersid.append(str(i))
        for j in usernums:
            j=str(j)+"%"
            pronums.append(j)
        doordict=dict(zip(usersid,pronums))

        return Response(doordict)


class DoorStatTimeView(generics.GenericAPIView):
    '''
        5 开门总时间统计
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|False|int|
        |start_addtime|申请添加开始时间|False|datetime|
        |end_addtime|申请添加结束时间|False|datetime|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |申请人用户id|所占百分比|Ture|float|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回门禁统计信息|
    '''
    module_perms = ['door_limits.door_view']
    queryset = Door_approval.objects.all()
    serializers = DoorStatSerialzer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DoorStatFilter

    def get(self, request, *args, **kwargs):
        queryset = Door_approval.objects.filter(door_status=1)
        usersids = []
        sumtime=0
        for i in queryset:
            usersids.append(i.user_id.id)
            sumtime += (i.door_end -i.door_start).seconds

        user_ids = set(usersids)
        user_ids = list(user_ids)
        usernums = []

        for user in user_ids:
            usertime = 0
            queryset1 = Door_approval.objects.filter(door_status=1,user_id=user)
            for i in queryset1:
                usertime += (i.door_end - i.door_start).seconds
            usernums.append(round(usertime / sumtime, 4) * 100)

        pronums = []
        usersid = []
        for i in user_ids:
            usersid.append(str(i))
        for j in usernums:
            j = str(j) + "%"
            pronums.append(j)
        doordict = dict(zip(usersid, pronums))

        return Response(doordict)

class DoorStatusInfoView(generics.ListAPIView):
    '''
    6  申请状态信息
    ---
    ### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    ### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |door_status|申请状态(1,'待审核'),(2,'已通过'),(3,'已拒绝')|--|int|

    ### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回占比信息|
    '''
    module_perms = []
    queryset = Door_approval.objects.all()
    serializer_class = DoorStatusInfoSerializer
