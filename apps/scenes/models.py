from django.db import models
from datetime import datetime

# Create your models here.

class Scene(models.Model):
    scene_addtime =models.DateTimeField(default=datetime.now,verbose_name="场景添加时间")
    scene_name = models.CharField(max_length=255,verbose_name="场景名称")
    scene_code = models.CharField(max_length=255,verbose_name="场景识别码")
    SCENE_STATUS=( (1,'在线'),(2,'离线') )
    scene_status = models.IntegerField(choices=SCENE_STATUS,verbose_name="场景状态")
    scene_gateway = models.CharField(max_length=255,null=True, verbose_name="网关密码")
    scene_level = models.IntegerField(verbose_name="场景优先级")

    class Meta():
        verbose_name = "场景表"
        permissions = (
            ('scene_view','场景浏览'),
            ('scene_contro','场景管理')
        )

    def __str__(self):
        return self.scene_name


EQUIPMENT_STATUS=(
    (1,"正常"),(2,"异常"),
)
EQUIPMENT_ONLINE=(
    (1,"在线"),(2,"离线"),
)

class Humidity(models.Model):
    humidity_insert_time = models.DateTimeField(default=datetime.now,verbose_name="湿度更新时间")
    humidity_value = models.FloatField(verbose_name="湿度值")
    humidity_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="湿度传感器状态")
    humidity_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='humidity')

    class Meta():
        verbose_name = "湿度表"
        ordering = ['-humidity_insert_time']


class Temperature(models.Model):
    temperature_insert_time = models.DateTimeField(default=datetime.now,verbose_name="温度更新时间")
    temperature_value = models.FloatField(verbose_name="温度值")
    temperature_status =models.IntegerField(choices=EQUIPMENT_STATUS,verbose_name="温度传感器状态")
    temperature_online =models.IntegerField(choices=EQUIPMENT_ONLINE,verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='temperature')
    class Meta():
        verbose_name = "温度表"
        ordering = ['-temperature_insert_time']


class Beam(models.Model):
    beam_insert_time = models.DateTimeField(default=datetime.now,verbose_name="光照更新时间")
    beam_value = models.FloatField(verbose_name="光照强度值")
    beam_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="光照强度状态")
    beam_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='beam')

    class Meta():
        verbose_name = "光照强度表"
        ordering = ['-beam_insert_time']


class Co2(models.Model):
    co2_insert_time = models.DateTimeField(default=datetime.now,verbose_name="co2更新时间")
    co2_value = models.FloatField(verbose_name="co2值")
    co2_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="co2传感器状态")
    co2_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='co2')

    class Meta():
        verbose_name = "co2的表"
        ordering = ['-co2_insert_time']


class Pm25(models.Model):
    pm25_insert_time = models.DateTimeField(default=datetime.now,verbose_name="pm25更新时间")
    pm25_value = models.FloatField(verbose_name="pm25值")
    pm25_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="pm25传感器状态")
    pm25_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='pm25')

    class Meta():
        verbose_name = "pm25表"
        ordering = ['-pm25_insert_time']



class Smoke(models.Model):
    smoke_insert_time = models.DateTimeField(default=datetime.now,verbose_name="烟雾更新时间")
    smoke_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="烟雾传感器状态")
    smoke_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='smoke')

    class Meta():
        verbose_name = "烟雾表"
        ordering = ['-smoke_insert_time']


class Flame(models.Model):
    flame_insert_time = models.DateTimeField(default=datetime.now,verbose_name="火光更新时间")
    flame_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="火光传感器状态")
    flame_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='flame')

    class Meta():
        verbose_name = "火光表"
        ordering = ['-flame_insert_time']


class Methane(models.Model):
    methane_insert_time = models.DateTimeField(default=datetime.now,verbose_name="甲烷更新时间")
    methane_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="甲烷传感器状态")
    methane_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='methane')

    class Meta():
        verbose_name = "甲烷表"
        ordering = ['-methane_insert_time']

class Alarmlamp(models.Model):
    alarmlamp_insert_time = models.DateTimeField(default=datetime.now,verbose_name="报警灯更新时间")
    alarmlamp_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="报警灯状态")
    alarmlamp_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='alarmlamp')

    class Meta():
        verbose_name = "报警灯表"
        ordering = ['-alarmlamp_insert_time']

class Alertor(models.Model):
    alertor_insert_time = models.DateTimeField(default=datetime.now,verbose_name="报警器更新时间")
    alertor_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="报警器状态")
    alertor_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='alertor')

    class Meta():
        verbose_name = "报警器表"
        ordering = ['-alertor_insert_time']



class Display(models.Model):
    display_insert_time = models.DateTimeField(default=datetime.now,verbose_name="显示器更新时间")
    display_content = models.CharField(max_length=255,verbose_name="显示内容")
    display_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="显示器状态")
    display_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态",default=1)
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='display')

    class Meta():
        verbose_name = "显示器表"
        ordering = ['-display_insert_time']


class Light(models.Model):
    light_insert_time = models.DateTimeField(default=datetime.now,verbose_name="灯光更新时间")
    light_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="灯光状态")
    light_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='light')

    class Meta():
        verbose_name = "灯光表"
        ordering = ['-light_insert_time']


class Pump(models.Model):
    pump_insert_time = models.DateTimeField(default=datetime.now,verbose_name="水泵更新时间")
    pump_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="水泵状态")
    pump_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='pump')

    class Meta():
        verbose_name = "水泵表"
        ordering = ['-pump_insert_time']


class Fan(models.Model):
    fan_insert_time = models.DateTimeField(default=datetime.now,verbose_name="风扇更新时间")
    fan_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="风扇状态")
    fan_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='fan')

    class Meta():
        verbose_name = "风扇表"
        ordering = ['-fan_insert_time']


class Unlocking(models.Model):
    unlocking_insert_time = models.DateTimeField(default=datetime.now,verbose_name="开锁更新时间")
    user_id = models.IntegerField(verbose_name="开锁用户")
    unlocking_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="开锁状态")
    unlocking_close_time = models.DateTimeField(verbose_name="开始结束时间（关门时间）")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='unlocking')

    class Meta():
        verbose_name = "开锁记录表"
        ordering = ['-unlocking_insert_time']


class Invade(models.Model):
    invade_insert_time = models.DateTimeField(default=datetime.now,verbose_name="入侵更新时间")
    invade_status = models.IntegerField(choices=EQUIPMENT_STATUS, verbose_name="入侵传感器状态")
    invade_online = models.IntegerField(choices=EQUIPMENT_ONLINE, verbose_name="在线状态")
    scene = models.ForeignKey('Scene',verbose_name="场景",on_delete=models.CASCADE,related_name='invade')

    class Meta():
        verbose_name = "入侵检测表"
        ordering = ['-invade_insert_time']

