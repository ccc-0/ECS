from rest_framework import serializers, validators
from django.contrib.auth.hashers import make_password
from .models import Users
from django.contrib.auth.models import Group,GroupManager

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('username','password','last_name','user_tel','user_gender',
                  'is_active','user_number',
                  # "地址",
                  'user_detail','user_picture')
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'id': {'required': True,'read_only': True},
            'password': {'required': True,'write_only': True, 'min_length': 6},
        }

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


# class UserGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields ='__all__'
#
# class UserGroupManagerSerializer(serializers.ModelSerializer):
#     group_id = UserGroupSerializer()
#     class Meta:
#         model = GroupManager
#         fields ='__all__'

class UserListSerializer(serializers.ModelSerializer):
    # user_group= UserGroupManagerSerializer()
    class Meta:
        model = Users
        fields = ('id','username','last_name','user_tel','user_gender',
                  'is_active','user_number','last_login',
                  'groups'
                  )
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'id': {'required': True,'read_only': True},
        }

class UserInfoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('username','password','last_name','user_tel','user_gender',
                  'is_active','user_number',
                  # "地址",
                  'user_detail','user_picture')
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'id': {'required': True,'read_only': True},
            'username': {'required': True, 'read_only': True},
            'password': {'required': True, 'read_only': True},
            'user_number': {'required': True, 'read_only': True},
        }

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ( 'is_active', )
        extra_kwargs = {  # 对模型已有参数重新设置和编辑
            'id': {'required': True,'read_only': True},
            'username': {'required': True, 'read_only': True},
            'password': {'required': True, 'read_only': True},
            'user_number': {'required': True, 'read_only': True},
        }
