from rest_framework import serializers, validators
from .models import *
from scenes.models import Scene


class LogSerializer(serializers.ModelSerializer):
    # 隐藏log_id字段
    log_id = serializers.HiddenField(
        default=serializers.IntegerField
    )
    class Meta:
        model = Logs
        fields = "__all__"

class LogSceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = ('scene_id', )


class LogModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Logs
        fields = ('log_module', )