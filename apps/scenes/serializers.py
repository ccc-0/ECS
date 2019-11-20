from rest_framework import serializers, validators
from .models import *
from alert.models import alarm_management


class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = "__all__"

#16个设备
class HumiditySerializers(serializers.ModelSerializer):
    class Meta:
        model = Humidity
        exclude = ('scene',)

class TemperatureSerializers(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        exclude = ('scene',)

class BeamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Beam
        exclude = ('scene',)

class Co2Serializers(serializers.ModelSerializer):
    class Meta:
        model = Co2
        exclude = ('scene',)

class PM25Serializers(serializers.ModelSerializer):
    class Meta:
        model = Pm25
        exclude = ('scene',)

class SmokeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Smoke
        exclude = ('scene',)

class FlameSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flame
        exclude = ('scene',)

class MethaneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Methane
        exclude = ('scene',)

class AlarmlampSerializers(serializers.ModelSerializer):
    class Meta:
        model = Alarmlamp
        exclude = ('scene',)

class AlertorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Alertor
        exclude = ('scene',)

class DisplaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Display
        exclude = ('scene',)

class LightSerializers(serializers.ModelSerializer):
    class Meta:
        model = Light
        exclude = ('scene',)

class PumpSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pump
        exclude = ('scene',)

class FanSerializers(serializers.ModelSerializer):
    class Meta:
        model = Fan
        exclude = ('scene',)

class UnlockingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Unlocking
        exclude = ('scene',)

class InvadeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invade
        exclude = ('scene',)

class SceneFireAlarmSerializers(serializers.ModelSerializer):
    sum_time = serializers.SerializerMethodField(source='get_sum_time', read_only=True)

    class Meta:
        model = alarm_management
        fields = ('sum_time', 'am_device', 'am_contene')

    def get_sum_time(self, obj):
        return obj.sum_time


class SceneDetailSerializer(serializers.ModelSerializer):
    # thenewtime = HumiditySerializers()
    class Meta:
        model = Scene
        fields = ( 'scene_name','scene_status', )

class EquipmentStautsSerializer(serializers.ModelSerializer):
    humidity = HumiditySerializers(many=True)
    temperature=TemperatureSerializers(many=True)
    beam=BeamSerializers(many=True)
    co2=Co2Serializers(many=True)
    pm25=PM25Serializers(many=True)
    smoke=SmokeSerializers(many=True)
    flame=FlameSerializers(many=True)
    methane=MethaneSerializers(many=True)
    alarmlamp=AlarmlampSerializers(many=True)
    alertor=AlertorSerializers(many=True)
    display=DisplaySerializers(many=True)
    light=LightSerializers(many=True)
    pump=PumpSerializers(many=True)
    fan=FanSerializers(many=True)
    unlocking=UnlockingSerializers(many=True)
    invade=InvadeSerializers(many=True)
    class Meta:
        model = Scene
        fields = ('humidity','temperature','beam','co2','pm25','smoke','flame','methane','alarmlamp','alertor',
                  'display','light','pump','fan','unlocking','invade',)


class HistFireDataSerializer(serializers.ModelSerializer):
    smoke=SmokeSerializers(many=True)
    flame=FlameSerializers(many=True)
    methane=MethaneSerializers(many=True)
    alarmlamp=AlarmlampSerializers(many=True)
    alertor=AlertorSerializers(many=True)
    class Meta:
        model = Scene
        fields = ('smoke','flame','methane','alarmlamp','alertor',)

class DisplaySerializers(serializers.ModelSerializer):
    display_insert_time = serializers.HiddenField(
        default=datetime.now()
    )
    class Meta:
        model = Display
        fields = '__all__'
        extra_kwargs = {
            'display_stutas': {'required': False, 'read_only': True},
            'display_online': {'required': False, 'read_only': True},
        }