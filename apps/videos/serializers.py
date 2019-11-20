from rest_framework import serializers, validators
from .models import *
from datetime import  datetime

class VideoSerializer(serializers.ModelSerializer):
    video_addtime = serializers.HiddenField(
        default=datetime.now()
    )
    class Meta:
        model = Video
        fields = "__all__"
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'id': {'required': True,'read_only': True},
            'video_addtime': {'required': True, 'read_only': True}
        }
