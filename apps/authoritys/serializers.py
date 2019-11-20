from rest_framework import serializers, validators
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,GroupManager

class GpCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model= Group
        fields='__all__'
