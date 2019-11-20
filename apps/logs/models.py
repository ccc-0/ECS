from django.db import models

from users.models import Users
from datetime import datetime
# Create your models here.

class Logs(models.Model):
    log_addtime = models.DateTimeField(default=datetime.now,verbose_name="日志添加时间")
    log_content =models.CharField(max_length=255,verbose_name="日志内容")
    user_id  =models.ForeignKey(Users,on_delete=models.CASCADE)
    log_module = models.CharField(max_length=255,verbose_name="所属模块")
    scene_id =models.IntegerField(verbose_name="所属场景")

    class Meta():
        verbose_name = "日志表"
        permissions = (
            ('log_view', '日志浏览'),
        )

