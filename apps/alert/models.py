from django.db import models

from scenes.models import Scene
from datetime import  datetime
# Create your models here.

class Alarm_type(models.Model):
    alarm_type_addtimt=models.DateTimeField(default=datetime.now,verbose_name="告警类型添加时间")
    alarm_type_name = models.CharField(max_length=255,verbose_name="告警类型名称")
    alarm_type_detail=models.CharField(max_length=255,verbose_name="告警类型说明")

    class Meta():
        verbose_name = "告警类型表"

    def __str__(self):
        return self.alarm_type_name

class Alarm_level(models.Model):
    alarm_level_addtimt = models.DateTimeField(default=datetime.now,verbose_name="告警级别添加时间")
    alarm_level_name = models.CharField(max_length=255, verbose_name="告警级别名称")
    alarm_level_detail = models.CharField(max_length=255, verbose_name="告警级别说明")

    class Meta():
        verbose_name = "告警级别表"

    def __str__(self):
        return self.alarm_level_name

class alarm_management(models.Model):
    am_addtime = models.DateTimeField(default=datetime.now,verbose_name="添加时间")
    am_type_id  =models.ForeignKey(Alarm_type,on_delete=models.CASCADE)
    am_level_id =models.ForeignKey(Alarm_level,on_delete=models.CASCADE)
    scene_id = models.ForeignKey(Scene,on_delete=models.CASCADE)
    am_device= models.CharField(max_length=255,verbose_name="告警设备")
    am_contene=models.CharField(max_length=255,verbose_name="告警内容")
    AM_STATUS = (
        (1,"待处理"),
        (2,"待审核"),
        (3,"审核通过"),
        (4,"审核未通过"),
    )
    am_status= models.IntegerField(choices=AM_STATUS,verbose_name="告警状态")
    am_deal_user = models.IntegerField(verbose_name="告警处理人")
    am_deal_time = models.DateTimeField(default=datetime.now,verbose_name="告警处理时间")
    am_deal_detail= models.CharField(max_length=255,verbose_name="告警处理说明")
    am_audit_user = models.IntegerField(verbose_name="告警审核人")
    am_audit_time = models.DateTimeField(default=datetime.now,verbose_name="告警审核时间")
    am_audit_detail = models.CharField(max_length=255, verbose_name="告警审核说明")

    class Meta():
        verbose_name = "告警表"
        permissions = (
            ('alarm_detail', '告警处理'),
            ('alarm_audit', '告警审核'),
        )

    def __str__(self):
        return self.am_contene
