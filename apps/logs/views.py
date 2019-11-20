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
from  .models import *
from  .serializers import *
from  .filters import *

# Create your views here.

#分页
class GoodsPagination(PageNumberPagination):
    page_size = 1  #每页显示条数
    page_size_query_param = 'page_size'
    max_page_size = 100 #每页最大条数
    page_query_param = 'p' #分页参数变量名

class LogListView(generics.ListAPIView):
    '''
        1 获取日志列表
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|False|int|
        |log_addtime_min|筛选日志添加开始时间|False|datetime|
        |log_addtime_max|筛选日志添加结束时间|False|datetime|
        |scene_id|所属场景|False|int|
        |log_module|所属模块False|int|
        |log_content|日志描述-用户查询|False|string|
        |ordering|以哪个字段排序，默认id|False|string|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|日志id|--|int|
        |log_addtime|日志添加时间|True|datetime|
        |log_content|日志内容|True|string|
        |log_module|所属模块|True|int|
        |scene_id|所属场景|True|int|
        |user_id |操作用户|True|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回日志列表|
    '''
    module_perms = ['logs.log_view']
    queryset = Logs.objects.all()
    serializer_class = LogSerializer
    # pagination_class = GoodsPagination  # 分页器

    # 过滤器使用
    # (DjangoFilterBackend过滤,SearchFilter搜索,OrderingFilter排序）
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    search_fields = ('log_content')  # 模糊查询- 搜索
    ordering_fields = ('-id')
    # 使用自定义过滤器
    filterset_class = LogFilter

class SceneAppertainView(generics.ListAPIView):
    '''
        3 所属场景信息
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |scene_name|场景名称|--|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回所属场景信息|
        '''
    module_perms = []
    queryset = Logs.objects.all()
    serializer_class =LogSceneSerializer

class ModuleAppertainView(generics.ListAPIView):
    '''
    4 所属模块信息
    ---
    ### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    ### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |log_module|模块信息|--|string|

    ### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回所属模块信息|
    '''
    module_perms = []
    queryset = Logs.objects.all()
    serializer_class =LogModuleSerializer

import xlwt
from io import BytesIO
# 用户数据导出成为excel文件
class LogsExcelFile(APIView):
    '''
        2 导出
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
    module_perms = ['logs.log_view']
    permission_classes = ()
    def get(self,request):
        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=logs.xls'# 文件名称
        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('logs-sheet')

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
        sheet.write(0, 0, '日志编号', style_heading)
        sheet.write(0, 1, '日志时间', style_heading)
        sheet.write(0, 2, '所属场景', style_heading)
        sheet.write(0, 3, '日志类型', style_heading)
        sheet.write(0, 4, '日志描述', style_heading)

        # 写入数据
        data_row = 1
        # User.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in Logs.objects.all():
            # 格式化datetime
            log_addtime = i.log_addtime.strftime('%Y-%m-%d')
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, log_addtime)
            sheet.write(data_row, 2, i.log_content)
            sheet.write(data_row, 3, i.log_module)
            sheet.write(data_row, 4, i.scene_id)
            data_row = data_row + 1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response

def AddLog(request,log_content,log_module,scene_id):
    '''
        添加日志
        当用户有操作时调用，生成日志
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
         |log_content|日志内容|Ture|string|
        |log_module|所属模块|Ture|int|
        |scene_id|所属场景|Ture|int|

        ### 响应字段说明(数据保存)
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|日志id|--|int|
        |log_addtime|日志添加时间|False|datetime|
        |log_content|日志内容|False|string|
        |user_id |操作用户|False|int|
        |log_module|所属模块False|int|
        |scene_id|所属场景|False|int|

    '''
    newlog = Logs()
    newlog.log_addtime=datetime.now()
    newlog.log_content=log_content
    newlog.user_id=request.user.id
    newlog.log_module=log_module
    newlog.scene_id=scene_id
    try:
        newlog.save()
    except:
        return False
    return True

