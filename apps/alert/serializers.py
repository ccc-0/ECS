from rest_framework import serializers, validators
from .models import *
from scenes.models import Scene

class Alarm_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm_type
        fields = "__all__"

class Alarm_levelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm_level
        fields = "__all__"

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = ('id','scene_name',)

class AlarmSceneSerializer(serializers.ModelSerializer):
    scene_id=SceneSerializer()
    class Meta:
        model = alarm_management
        fields = ('scene_id', )

class AlarmTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm_type
        fields = ('id','alarm_type_name',)
class AlarmTypeInfoSerializer(serializers.ModelSerializer):
    am_type_id= AlarmTypeSerializer()
    class Meta:
        model = alarm_management
        fields = ('am_type_id', )

class AlarmLeveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm_level
        fields = ('id','alarm_level_name',)
class AlarmLeveInfoSerializer(serializers.ModelSerializer):
    am_level_id= AlarmLeveSerializer()
    class Meta:
        model = alarm_management
        fields = ('am_level_id', )

class AlarmStatusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = alarm_management
        fields = ('am_status', )

class AlarmSerializer(serializers.ModelSerializer):
    am_type_id = Alarm_typeSerializer()
    am_level_id= Alarm_levelSerializer()
    scene_id= SceneSerializer()
    class Meta:
        model = alarm_management
        fields = "__all__"
        # extra_kwargs = { #对模型已有参数重新设置和编辑
        #     'am_addtime':{'required':False,'read_only':True}
        # }

class AlarmDealUpdateSerializer(serializers.ModelSerializer):
    am_deal_time= serializers.HiddenField(
        default=datetime.now()
    )
    am_status=serializers.HiddenField( default=2 )
    class Meta:
        model = alarm_management
        fields = ("am_deal_time",'am_deal_detail','am_status',)

class AlarmStatusUpdateSerializer(serializers.ModelSerializer):
    am_deal_time= serializers.HiddenField(
        default=datetime.now()
    )

    class Meta:
        model = alarm_management
        fields = ("am_deal_time", 'am_deal_detail', 'am_status',)




