from datetime import timedelta
from django.db import connection
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
from  .filters import *
from  .schema import *
from alert.models import alarm_management

# Create your views here.
#分页
class GoodsPagination(PageNumberPagination):
    page_size = 1  #每页显示条数
    page_size_query_param = 'page_size'
    max_page_size = 100 #每页最大条数
    page_query_param = 'p' #分页参数变量名


class SceneCreateView(generics.CreateAPIView):
    '''
        1 新建场景
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |scene_addtime|场景添加时间-用户查询|False|datetime|
        |scene_name|场景名称|False|string|
        |scene_code|场景识别码|False|string|
        |scene_status|场景状态(1,'在线'),(2,'离线')|True|int|
        |scene_gateway|网关密码|Ture|string|
        |scene_level|场景优先级|True|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|--|int|
        |scene_addtime|场景添加时间-用户查询|False|datetime|
        |scene_name|场景名称|False|string|
        |scene_code|场景识别码|False|string|
        |scene_status|场景状态(1,'在线'),(2,'离线')|True|int|
        |scene_gateway|网关密码|Ture|string|
        |scene_level|场景优先级|True|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回添加场景|
        '''
    module_perms = ['scenes.scene_contro']
    serializer_class = SceneSerializer

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

class SceneListView(generics.ListAPIView):
    '''
        2 场景列表
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|--|int|
        |scene_addtime|场景添加时间-用户查询|False|datetime|
        |scene_name|场景名称|False|string|
        |scene_code|场景识别码|False|string|
        |scene_status|场景状态(1,'在线'),(2,'离线')|True|int|
        |scene_gateway|网关密码|Ture|string|
        |scene_level|场景优先级|True|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回场景列表|
        '''
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    # permission_classes = ()  # 不需要身份验证
    module_perms=['scenes.scene_view'] # 判断是否有浏览场景权限（app_label.codename)

class SceneDeleteView(generics.GenericAPIView):
    '''
        3 删除场景
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|Ture|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |mesage|删除成功|--|--|
        |code||--|--|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回添加场景|
        '''
    module_perms = ['scenes.scene_contro']
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

    def get(self,request,pk):
        try:
            obj = Scene.objects.get(pk=pk)
            obj.delete()
        except:
            return Response(data={'code': 400, 'message': '删除失败'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code':200,'message':'删除成功'},status=status.HTTP_200_OK)

class SceneUpdateView(generics.GenericAPIView,mixins.UpdateModelMixin):
    '''
        4 修改场景信息
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|Ture|int|
        |scene_addtime|场景添加时间-用户查询|False|datetime|
        |scene_name|场景名称|False|string|
        |scene_code|场景识别码|False|string|
        |scene_status|场景状态(1,'在线'),(2,'离线')|True|int|
        |scene_gateway|网关密码|Ture|string|
        |scene_level|场景优先级|True|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|--|int|
        |scene_addtime|场景添加时间-用户查询|False|datetime|
        |scene_name|场景名称|False|string|
        |scene_code|场景识别码|False|string|
        |scene_status|场景状态(1,'在线'),(2,'离线')|True|int|
        |scene_gateway|网关密码|Ture|string|
        |scene_level|场景优先级|True|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回场景信息|
        '''
    module_perms = ['scenes.scene_contro']
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

    def post(self, request, *args, **kwargs):
        try:
            self.update(request, *args, **kwargs)  # 调用UpdateModelMixin方法
        except:
            return Response(data={'code': 400, 'message': '修改失败' }, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'code': 200, 'message': '修改成功'}, status=status.HTTP_200_OK)


class SceneBrowseView(generics.ListAPIView):
    '''
        5 场景浏览接口
        ---
        ### 参数说明

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|--|int|
        |scene_addtime|场景添加时间-用户查询|False|datetime|
        |scene_name|场景名称|False|string|
        |scene_code|场景识别码|False|string|
        |scene_status|场景状态(1,'在线'),(2,'离线')|True|int|
        |scene_gateway|网关密码|Ture|string|
        |scene_level|场景优先级|True|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回所有场景信息|
        '''
    module_perms = ['scenes.scene_view']
    queryset = Scene.objects.all()
    serializer_class =SceneDetailSerializer

class EquipmentStautsView(APIView):
    '''
      6 查看设备状态
      ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|场景id|Ture|int|


      ### 响应字段说明
      |字段名称|描述|必须|类型|
      |--|--|--|--|
      |humidity|湿度|--|string|
      |temperature|温度|--|string|
      |beam|光照|--|string|
      |co2|Co2|--|string|
      |PM25|PM2.5|--|string|
      |smoke|烟雾|--|string|
      |flame|火光|--|string|
      |methane|甲烷|--|string|
      |alarmlamp|报警灯|--|string|
      |alertor|报警器|--|string|
      |display|显示器|--|string|
      |light|灯光|--|string|
      |pump|水泵|--|string|
      |fan|风扇|--|string|
      |Unlocking|开锁记录|--|string|
      |invade|入侵检测|--|string|

      ### 响应消息：
      |Http响应码|原因|响应模型|
      |--|--|--|
      |200|请求成功|返回所有已有设备信息|
      '''
    module_perms = ['scenes.scene_view']
    schema = SceneListSchema
    pagination_class = None  # 不需要分页时

    def get(self, request):
        scene_id = self.request.query_params.get('scene_id', '')
        device_status_dict = {}
        if scene_id:
            try:
                humidity = Humidity.objects.filter(scene_id=scene_id)[0]
                device_status_dict['humidity'] = HumiditySerializers(humidity).data
                temperature = Temperature.objects.filter(scene_id=scene_id)[0]
                device_status_dict['temperature'] = TemperatureSerializers(temperature).data
                beam = Beam.objects.filter(scene_id=scene_id)[0]
                device_status_dict['beam'] = BeamSerializers(beam).data
                co2 = Co2.objects.filter(scene_id=scene_id)[0]
                device_status_dict['co2'] = Co2Serializers(co2).data
                PM25 = Pm25.objects.filter(scene_id=scene_id)[0]
                device_status_dict['PM25'] = PM25Serializers(PM25).data
                smoke = Smoke.objects.filter(scene_id=scene_id)[0]
                device_status_dict['smoke'] = SmokeSerializers(smoke).data
                flame = Flame.objects.filter(scene_id=scene_id)[0]
                device_status_dict['flame'] = FlameSerializers(flame).data
                methane = Methane.objects.filter(scene_id=scene_id)[0]
                device_status_dict['methane'] = MethaneSerializers(methane).data
                alarmlamp = Alarmlamp.objects.filter(scene_id=scene_id)[0]
                device_status_dict['alarmlamp'] = AlarmlampSerializers(alarmlamp).data
                alertor = Alertor.objects.filter(scene_id=scene_id)[0]
                device_status_dict['alertor'] = AlertorSerializers(alertor).data
                display = Display.objects.filter(scene_id=scene_id)[0]
                device_status_dict['display'] = DisplaySerializers(display).data
                light = Light.objects.filter(scene_id=scene_id)[0]
                device_status_dict['light'] = LightSerializers(light).data
                pump = Pump.objects.filter(scene_id=scene_id)[0]
                device_status_dict['pump'] = PumpSerializers(pump).data
                fan = Fan.objects.filter(scene_id=scene_id)[0]
                device_status_dict['fan'] = FanSerializers(fan).data
                unlocking = Unlocking.objects.filter(scene_id=scene_id)[0]
                device_status_dict['unlocking'] = UnlockingSerializers(unlocking).data
                invade = Invade.objects.filter(scene_id=scene_id)[0]
                device_status_dict['invade'] = InvadeSerializers(invade).data
            except:
                return Response(data={'message': '有的表暂无数据','code':400})
        else:
            try:
                humidity = Humidity.objects.filter(scene_id=1)[0]
                device_status_dict['humidity'] = HumiditySerializers(humidity).data
                temperature = Temperature.objects.filter(scene_id=1)[0]
                device_status_dict['temperature'] = TemperatureSerializers(temperature).data
                beam = Beam.objects.filter(scene_id=1)[0]
                device_status_dict['beam'] = BeamSerializers(beam).data
                co2 = Co2.objects.filter(scene_id=1)[0]
                device_status_dict['co2'] = Co2Serializers(co2).data
                PM25 = Pm25.objects.filter(scene_id=1)[0]
                device_status_dict['PM25'] = PM25Serializers(PM25).data
                smoke = Smoke.objects.filter(scene_id=1)[0]
                device_status_dict['smoke'] = SmokeSerializers(smoke).data
                flame = Flame.objects.filter(scene_id=1)[0]
                device_status_dict['flame'] = FlameSerializers(flame).data
                methane = Methane.objects.filter(scene_id=1)[0]
                device_status_dict['methane'] = MethaneSerializers(methane).data
                alarmlamp = Alarmlamp.objects.filter(scene_id=1)[0]
                device_status_dict['alarmlamp'] = AlarmlampSerializers(alarmlamp).data
                alertor = Alertor.objects.filter(scene_id=1)[0]
                device_status_dict['alertor'] = AlertorSerializers(alertor).data
                display = Display.objects.filter(scene_id=1)[0]
                device_status_dict['display'] = DisplaySerializers(display).data
                light = Light.objects.filter(scene_id=1)[0]
                device_status_dict['light'] = LightSerializers(light).data
                pump = Pump.objects.filter(scene_id=1)[0]
                device_status_dict['pump'] = PumpSerializers(pump).data
                fan = Fan.objects.filter(scene_id=1)[0]
                device_status_dict['fan'] = FanSerializers(fan).data
                unlocking = Unlocking.objects.filter(scene_id=1)[0]
                device_status_dict['unlocking'] = UnlockingSerializers(unlocking).data
                invade = Invade.objects.filter(scene_id=1)[0]
                device_status_dict['invade'] = InvadeSerializers(invade).data
            except:
                return Response(data={'message': '有的表暂无数据','code':400})
        return Response(device_status_dict)


#定义函数
def calculate_fire_history(end_time, start_time, scene_id, sql):
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)  # 转化成时间加一天
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)  # 开始时间减一天
    end_time = datetime.strftime(end_time, '%Y-%m-%d')  # 结束时间去掉时分秒并转化成字符串
    start_time = datetime.strftime(start_time, '%Y-%m-%d')
    cursor = connection.cursor()
    sql = sql.format(start_time, end_time, scene_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    end_time_date = datetime.strptime(end_time, '%Y-%m-%d')  # 结束时间转化成时间类型
    start_time_date = datetime.strptime(start_time, '%Y-%m-%d') + timedelta(days=1)
    while end_time_date > start_time_date:
        end_time_date = end_time_date - timedelta(days=1)  # 减一天
        end_time = datetime.strftime(end_time_date, '%Y-%m-%d')  # 转化成字符串
        if result:
            for j in result:
                if end_time in j:
                    data[end_time] = '有'
                    break
                else:
                    data[end_time] = '无'
        else:
            data[end_time] = '无'
    return data

class SceneFireHistoryView(APIView):
    '''
     7 场景消防设备数据统计图
     ---
       ### 参数说明
       |字段名称|描述|必须|类型|
       |--|--|--|--|
       |start_time|统计开始时间|False|datetime|
       |end_time|统计结束时间|False|datetime|
       |scene_id|场景id|Ture|int|


     ### 响应字段说明
     |字段名称|描述|必须|类型|
     |--|--|--|--|
     ||占比|--|dict|

     ### 响应消息：
     |Http响应码|原因|响应模型|
     |--|--|--|
     |200|请求成功|返回统计信息|
     '''
    module_perms = ['scenes.scene_view']
    schema = SceneFireHistorySchema

    def post(self, request):
        # 传了是字符串字符串，不传是当前时间字符串
        end_time = self.request.query_params.get('end_time', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        start_time = self.request.query_params.get('start_time', datetime.strftime(datetime.now() - timedelta(weeks=1), "%Y-%m-%d %H:%M:%S"))
        scene_id = self.request.query_params.get('scene_id')
        result_dict = {}
        smoke_sql = """SELECT DATE_FORMAT(smoke_insert_time,"%Y-%m-%d") from scenes_smoke 
                    where smoke_status = 2 and smoke_insert_time> '{}' and smoke_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(smoke_insert_time,"%Y-%m-%d")
                    """
        result_dict['smoke'] = calculate_fire_history(end_time, start_time, scene_id, smoke_sql)
        flame_sql = """SELECT DATE_FORMAT(flame_insert_time,"%Y-%m-%d") from scenes_flame 
                    where flame_status = 2 and flame_insert_time> '{}' and flame_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(flame_insert_time,"%Y-%m-%d")
                    """
        result_dict['flame'] = calculate_fire_history(end_time, start_time, scene_id, flame_sql)
        methane_sql = """SELECT DATE_FORMAT(methane_insert_time,"%Y-%m-%d") from scenes_methane 
                    where methane_status = 2 and methane_insert_time> '{}' and methane_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(methane_insert_time,"%Y-%m-%d")
                    """
        result_dict['methane'] = calculate_fire_history(end_time, start_time, scene_id, methane_sql)
        alarmlamp_sql = """SELECT DATE_FORMAT(alarmlamp_insert_time,"%Y-%m-%d") from scenes_alarmlamp 
                        where alarmlamp_status = 2 and alarmlamp_insert_time> '{}' and alarmlamp_insert_time < '{}' and scene_id = {}
                        GROUP BY DATE_FORMAT(alarmlamp_insert_time,"%Y-%m-%d")
                        """
        result_dict['alarmlamp'] = calculate_fire_history(end_time, start_time, scene_id, alarmlamp_sql)
        alertor_sql = """SELECT DATE_FORMAT(alertor_insert_time,"%Y-%m-%d") from scenes_alertor 
                    where alertor_status = 2 and alertor_insert_time> '{}' and alertor_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(alertor_insert_time,"%Y-%m-%d")
                    """
        result_dict['alertor'] = calculate_fire_history(end_time, start_time, scene_id, alertor_sql)
        return Response(result_dict)

class SceneFireAlarmView(generics.ListAPIView):
    '''
        8 场景消防设备报警统计表
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |start_time|统计开始时间|False|datetime|
       |end_time|统计结束时间|False|datetime|
       |scene_id|场景id|Ture|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |smoke-alarm|烟雾|--|string|
        |flame-alarm|火光|--|string|
        |methane-alarm|甲烷|--|string|
        |alarmlamp-alarm|报警灯|--|string|
        |alertor-alarm|报警器|--|string|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回所有消防设备报警信息|
        '''
    module_perms = ['scenes.scene_view']
    serializer_class = SceneFireAlarmSerializers
    schema = SceneFireHistorySchema

    def get_queryset(self):
        start_time = self.request.query_params.get('start_time', '1970-01-01 00:00:00')
        end_time = self.request.query_params.get('end_time', datetime.now())
        scene_id = self.request.query_params.get('scene_id')
        queryset = alarm_management.objects.filter(scene_id=scene_id, am_addtime__range=(start_time, end_time), am_type_id=2)
        for i in queryset:
            if i.am_deal_time:
                i.sum_time = round((i.am_deal_time - i.am_addtime).total_seconds() / 60, 2)
            else:
                i.sum_time = round((datetime.now() - i.am_addtime).total_seconds() / 60, 2)
        return queryset


class SceneEnvironmentHistoryView1(generics.ListAPIView):
    '''11 场景环境设备数据统计图'''

    module_perms = ['scenes.scene_view']
    schema = SceneListSchema
    serializer_class = HumiditySerializers
    filter_backends = (DjangoFilterBackend, )
    filterset_class = HumidityFilter
    def get_queryset(self):
        # 1
        scene_id = self.request.query_params.get('scene','')
        queryset = Humidity.objects.filter(scene=scene_id)
        print(queryset)

#定义函数
def calculate_environment_history(end_time, start_time, scene_id, sql):
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)  # 转化成时间加一天
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') - timedelta(days=1)  # 开始时间减一天
    end_time = datetime.strftime(end_time, '%Y-%m-%d')  # 结束时间去掉时分秒并转化成字符串
    start_time = datetime.strftime(start_time, '%Y-%m-%d')
    cursor = connection.cursor()
    sql = sql.format(start_time, end_time, scene_id)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    data = {}
    end_time_date = datetime.strptime(end_time, '%Y-%m-%d')  # 结束时间转化成时间类型
    start_time_date = datetime.strptime(start_time, '%Y-%m-%d') + timedelta(days=1)
    while end_time_date > start_time_date:
        end_time_date = end_time_date - timedelta(days=1)  # 减一天
        end_time = datetime.strftime(end_time_date, '%Y-%m-%d')  # 转化成字符串
        if result:
            for j in result:
                if end_time in j:
                    data[end_time] = j[1]
                    break
                else:
                    data[end_time] = 0
        else:
            data[end_time] = 0
    return data

class SceneEnvironmentHistoryView(APIView):
    '''
        11 场景环境设备数据统计图
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |start_time|统计开始时间|False|datetime|
       |end_time|统计结束时间|False|datetime|
       |scene_id|场景id|Ture|int|
        |scene_env_device|传感器设备('湿度传感器','温度传感器','光照强度传感器','Co2传感器','Pm2.5传感器')|Ture|string|


        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |humidity|湿度|--|dict|
        |temperature|温度|--|dict|
        |beam|光照|--|dict|
        |co2|Co2|--|dict|
        |PM25|PM2.5|--|dict|

         ### 注意说明
        - 1 字典中的数据为每个设备的各个日期统计数据

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回所有设备统计信息|
        '''
    module_perms = ['scenes.scene_view']
    schema = SceneEnvironmentHistorySchema

    def post(self, request):
        end_time = self.request.query_params.get('end_time', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        start_time = self.request.query_params.get('start_time', datetime.strftime(datetime.now() - timedelta(weeks=1), "%Y-%m-%d %H:%M:%S"))
        scene_id = self.request.query_params.get('scene_id')
        scene_env_device = self.request.query_params.get('scene_env_device')
        result_dict = {}
        if scene_env_device == '湿度传感器':
            humidity_sql = """SELECT DATE_FORMAT(humidity_insert_time,"%Y-%m-%d"),avg(humidity_value) from scenes_humidity 
                        where humidity_insert_time> '{}' and humidity_insert_time < '{}' and scene_id = {}
                        GROUP BY DATE_FORMAT(humidity_insert_time,"%Y-%m-%d")
                        """
            result_dict['humidity'] = calculate_environment_history(end_time, start_time, scene_id, humidity_sql)
        if scene_env_device == '温度传感器':
            temperature_sql = """SELECT DATE_FORMAT(temperature_insert_time,"%Y-%m-%d"),avg(temperature_value) from scenes_temperature
                        where temperature_insert_time> '{}' and temperature_insert_time < '{}' and scene_id = {}
                        GROUP BY DATE_FORMAT(temperature_insert_time,"%Y-%m-%d")
                        """
            result_dict['temperature'] = calculate_environment_history(end_time, start_time, scene_id, temperature_sql)
        if scene_env_device == '光照强度传感器':
            berm_sql = """SELECT DATE_FORMAT(berm_insert_time,"%Y-%m-%d"),avg(berm_value) from scenes_beam
                        where berm_insert_time> '{}' and berm_insert_time < '{}' and scene_id = {}
                        GROUP BY DATE_FORMAT(berm_insert_time,"%Y-%m-%d")
                        """
            result_dict['berm'] = calculate_environment_history(end_time, start_time, scene_id, berm_sql)
        if scene_env_device == 'Co2传感器':
            co2_sql = """SELECT DATE_FORMAT(co2_insert_time,"%Y-%m-%d"),avg(co2_value) from scenes_co2
                        where co2_insert_time> '{}' and co2_insert_time < '{}' and scene_id = {}
                        GROUP BY DATE_FORMAT(co2_insert_time,"%Y-%m-%d")
                        """
            result_dict['co2'] = calculate_environment_history(end_time, start_time, scene_id, co2_sql)
        if scene_env_device == 'Pm2.5传感器':
            pm25_sql = """SELECT DATE_FORMAT(pm25_insert_time,"%Y-%m-%d"),avg(pm25_value) from scenes_pm25
                        where pm25_insert_time> '{}' and pm25_insert_time < '{}' and scene_id = {}
                        GROUP BY DATE_FORMAT(pm25_insert_time,"%Y-%m-%d")
                        """
            result_dict['pm25'] = calculate_environment_history(end_time, start_time, scene_id, pm25_sql)
        return Response(result_dict)

class SceneEnvironmentAlarmView(generics.ListAPIView):
    '''
        12 场景环境设备报警统计表
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |start_time|统计开始时间|False|datetime|
        |end_time|统计结束时间|False|datetime|
        |scene_id|场景id|Ture|int|
        |scene_env_device|传感器设备('湿度传感器','温度传感器','光照强度传感器','Co2传感器','Pm2.5传感器')|Ture|string|


        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |humidity|湿度|--|dict|
        |temperature|温度|--|dict|
        |beam|光照|--|dict|
        |co2|Co2|--|dict|
        |PM25|PM2.5|--|dict|

        ### 注意说明
        - 1 字典中的数据为每个设备的报警信息

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回所有设备报警信息|
        '''
    module_perms = ['scenes.scene_view']
    serializer_class = SceneFireAlarmSerializers
    schema = SceneEnvironmentAlarmSchema

    def get_queryset(self):
        start_time = self.request.query_params.get('start_time', '1970-01-01 00:00:00')
        end_time = self.request.query_params.get('end_time', datetime.now())
        scene_id = self.request.query_params.get('scene_id')
        scene_env_device = self.request.query_params.get('scene_env_device')
        queryset = alarm_management.objects.filter(scene_id=scene_id, am_addtime__range=(start_time, end_time), am_device=scene_env_device)
        for i in queryset:
            if i.am_deal_time:
                i.sum_time = round((i.am_deal_time - i.am_addtime).total_seconds() / 60, 2)
            else:
                i.sum_time = round((datetime.now() - i.am_addtime).total_seconds() / 60, 2)
        return queryset


# 显示屏内容
class SceneDisplayCreateView(generics.CreateAPIView):
    '''13 显示屏内容
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |display_content|显示器内容|True|int|
        |display_status|显示器状态(1,"正常"),(2,"异常"),|True|int|
        |scene|场景id|Ture|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|显示器id|--|int|
        |display_insert_time|显示器更新时间|Ture|--datetime|
        |display_content|显示器内容|True|int|
        |display_status|显示器状态(1,"正常"),(2,"异常"),|Ture|int|
        |display_online|在线状态,默认在线(1,"在线"),(2,"离线"),|Ture|int|
        |scene|场景id|Ture|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回显示器列表|
    '''

    module_perms = ['scenes.scene_view']
    serializer_class = DisplaySerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={'code': 400, 'message': '新增失败'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        res.data['code'] = 200
        res.data['message'] = '新增成功'
        return res


class SceneEquipmentHistoryView(APIView):
    '''
        14水泵、灯光、风扇数据统计图
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |start_time|统计开始时间|False|datetime|
        |end_time|统计结束时间|False|datetime|
        |scene_id|场景id|Ture|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |light|灯光传感器|--|dict|
        |pump|水泵|--|dict|
        |fan|风机|--|dict|

        ### 注意说明
        - 1 字典中均为个传感器的各个日期的统计数据

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回统计数据|
        '''
    module_perms = ['scenes.scene_view']
    schema = SceneFireHistorySchema

    def post(self, request):
        # 传了是字符串字符串，不传是当前时间字符串
        end_time = self.request.query_params.get('end_time', datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))
        start_time = self.request.query_params.get('start_time', datetime.strftime(datetime.now() - timedelta(weeks=1), "%Y-%m-%d %H:%M:%S"))
        scene_id = self.request.query_params.get('scene_id')
        result_dict = {}
        light_sql = """SELECT DATE_FORMAT(light_insert_time,"%Y-%m-%d") from scenes_light 
                    where light_status = 2 and light_insert_time> '{}' and light_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(light_insert_time,"%Y-%m-%d")
                    """
        result_dict['light'] = calculate_fire_history(end_time, start_time, scene_id, light_sql)
        pump_sql = """SELECT DATE_FORMAT(pump_insert_time,"%Y-%m-%d") from scenes_pump 
                    where pump_status = 2 and pump_insert_time> '{}' and pump_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(pump_insert_time,"%Y-%m-%d")
                    """
        result_dict['pump'] = calculate_fire_history(end_time, start_time, scene_id, pump_sql)
        fan_sql = """SELECT DATE_FORMAT(fan_insert_time,"%Y-%m-%d") from scenes_fan 
                    where fan_status = 2 and fan_insert_time> '{}' and fan_insert_time < '{}' and scene_id = {}
                    GROUP BY DATE_FORMAT(fan_insert_time,"%Y-%m-%d")
                    """
        result_dict['fan'] = calculate_fire_history(end_time, start_time, scene_id, fan_sql)
        return Response(result_dict)

class SceneEquipmentOpenView(APIView):
    '''
        15 水泵、灯光、风扇数据打开占比图
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |start_time|统计开始时间|False|datetime|
        |end_time|统计结束时间|False|datetime|
        |scene_id|场景id|Ture|int|


       ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |light|灯光传感器|--|dict|
        |pump|水泵|--|dict|
        |fan|风机|--|dict|

        ### 注意说明
        - 1 字典中均为个传感器的打开次数占比

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回用户列表|
        '''
    module_perms = ['scenes.scene_view']
    schema = SceneFireHistorySchema

    def post(self, request):
        start_time = self.request.query_params.get('start_time', '1970-01-01 00:00:00')
        end_time = self.request.query_params.get('end_time', datetime.now())
        scene_id = self.request.query_params.get('scene_id')
        light = Light.objects.filter(light_insert_time__range=(start_time, end_time), scene_id=scene_id)
        light_count = 0
        for i in range(len(light)-1):
            if light[i].light_online != light[i+1].light_online:
                if light[i].light_online == 1:
                    light_count += 1
        if light[len(light)-1].light_online == 1:
            light_count += 1
        pump = Pump.objects.filter(pump_insert_time__range=(start_time, end_time), scene_id=scene_id)
        pump_count = 0
        for i in range(len(pump)-1):
            if pump[i].pump_online != pump[i+1].pump_online:
                if pump[i].pump_online == 1:
                    pump_count += 1
        if pump[len(pump)-1].pump_online == 1:
            pump_count += 1
        fan = Fan.objects.filter(fan_insert_time__range=(start_time, end_time), scene_id=scene_id)
        fan_count = 0
        for i in range(len(fan) - 1):
            if fan[i].fan_online != fan[i + 1].fan_online:
                if fan[i].fan_online == 1:
                    fan_count += 1
        if fan[len(fan)-1].fan_online == 1:
            fan_count += 1
        light_precent = str(round(light_count / (light_count + pump_count + fan_count), 4)*100) + '%'
        pump_precent = str(round(pump_count / (light_count + pump_count + fan_count), 4) * 100) + '%'
        fan_precent = str(round(fan_count / (light_count + pump_count + fan_count), 4) * 100) + '%'
        light_data = []
        light_data.append(light_count)
        light_data.append(light_precent)
        pump_data = []
        pump_data.append(pump_count)
        pump_data.append(pump_precent)
        fan_data = []
        fan_data.append(fan_count)
        fan_data.append(fan_precent)
        result = {}
        result['light'] = light_data
        result['pump'] = pump_data
        result['fan'] = fan_data
        return Response(result)


class SceneUnlockingView(generics.ListAPIView):
    '''
        16开锁记录
        ---
        ### 参数说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |page|分页|True|int|
        |scene_id|场景id|Ture|int|

        ### 响应字段说明
        |字段名称|描述|必须|类型|
        |--|--|--|--|
        |id|视频id|--|int|
        |unlocking_insert_time|开锁更新时间|--|datetime|
        |user_id|开锁用户|--|int|
        |unlocking_status|开锁状态|--|int|
        |unlocking_close_time|开始结束时间|--|datetime|
        |scene|场景id|--|int|

        ### 响应消息：
        |Http响应码|原因|响应模型|
        |--|--|--|
        |200|请求成功|返回最新的五条开锁数据|
        '''
    module_perms = ['scenes.scene_view']
    queryset = Unlocking.objects.all()
    schema = SceneListSchema
    serializer_class = UnlockingSerializers

    def get_queryset(self):
        scene_id = self.request.query_params.get('scene')
        queryset = Unlocking.objects.filter(scene_id=scene_id)
        if len(queryset) < 5:
            return queryset
        else:
            return queryset[:5]

