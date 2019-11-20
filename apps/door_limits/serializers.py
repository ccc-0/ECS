from rest_framework import serializers, validators
from .models import *


class DoorLimitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door_approval
        fields = "__all__"
        # extra_kwargs = { #对模型已有参数重新设置和编辑
        #     'door_addtime':{'required':False,'read_only':True}
        # }

        # #验证器：收藏夹用户和商品的联合唯一限制
        # validators=[
        #     validators.UniqueTogetherValidator(
        #         queryset=Door_approval.objects.all(),
        #         fields = ('user','goods'),
        #         message="我爱你，该商品已收藏，亲，请勿重复收藏哦"
        #     )
        # ]

class DoorLimitsCreateSerializer(serializers.ModelSerializer):
    # # 隐藏user字段并且赋值为当前登录用户
    user_id = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Door_approval
        fields = ['user_id',"door_start",'door_end','door_follownum','door_follow','door_detail','scene_id']
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'door_id': {'required':True, 'read_only': True},
            'door_addtime': {'required': False, 'read_only': True}
        }

class DoorLimitsUpdateSerializer(serializers.ModelSerializer):

    door_audittime= serializers.HiddenField(
        default=datetime.now()
    )
    class Meta:
        model = Door_approval
        fields = ('door_audittime',"door_feedback",'door_status')


class DoorStatSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Door_approval
        fields = '__all__'

class DoorStatusInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Door_approval
        fields = ('door_status', )


