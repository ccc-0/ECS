from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
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
from  .models import *
from  .serializers import *

# Create your views here.
#新增
class AddVideoView(generics.CreateAPIView):
    '''
        1 添加视频
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |video_name|视频名称|True|string|
        |video_detail|视频描述|True|string|
        |video_address|视频地址|True|string|
        |video_user|用户名|True|string|
        |video_passwd|密码|True|string|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|视频id|--|int|
        |video_addtime|视频添加时间|True|datatime|
        |video_name|视频名称|True|string|
        |video_detail|视频描述|True|string|
        |video_address|视频地址|True|string|
        |video_user|用户名|True|string|
        |video_passwd|密码|True|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |201|添加成功|返回视频信息|
    '''
    module_perms = ['videos.video_contro']
    serializer_class = VideoSerializer

    # 自定义返回结果
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # 失败信息的定制
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '添加视频失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 成功后返回信息的定制
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        res.data['code'] = 201
        res.data['message'] = "亲，添加成功了哦"
        return res

#视频列表
class VideoListView(generics.ListAPIView):
    '''
        2 视频列表
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|False|int|

        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|视频id|--|int|
        |video_addtime|视频添加时间|False|datatime|
        |video_name|视频名称|False|string|
        |video_detail|视频描述|False|string|

        #### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |201|添加成功|返回视频信息|
    '''
    module_perms = ['videos.video_view']
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # def get_queryset(self):
        # queryset = Video.objects.filter()
        # return queryset

#删除   删除-get
class VideoDeleteView(generics.GenericAPIView):
    '''
        3 删除视频
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|视频id|--|int|

        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        #### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|删除成功||
    '''
    module_perms = ['videos.video_contro']
    queryset =  Video.objects.all()
    serializer_class = VideoSerializer

    def get(self,request,pk):
        #获取地址url中的参数
        name = self.kwargs.get('pk','')
        try:
            obj = Video.objects.get(pk=pk)   #使用get获取单条数据
            obj.delete()
        except:
            return Response(data={'code': 400, 'message': '亲，删除失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'亲，删除成功'},status=status.HTTP_200_OK)

#更改 post
class VideoUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    '''
        4 修改视频信息
        ---
        #### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|视频id|True|int|
        |video_name|视频名称|False|string|
        |video_detail|视频描述|False|string|
        |video_address|视频地址|False|string|
        |video_user|用户名|False|string|
        |video_passwd|密码|False|string|

        #### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        #### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|修改成功| |
    '''
    module_perms = ['videos.video_contro']
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    #数据编辑用post方式
    def post(self,request,*args,**kwargs):
        # print('request:',request)
        # print(kwargs)
        try:
            self.update(request,*args,**kwargs)  #调用UpdateModelMixin方法
        except:
            return Response(data={'code':400,'message':'修改失败',},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'修改成功'},status=status.HTTP_200_OK)

