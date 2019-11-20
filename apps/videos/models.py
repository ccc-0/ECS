from django.db import models

# Create your models here.

class Video(models.Model):
    video_addtime = models.DateTimeField(verbose_name="视频添加时间")
    video_name = models.CharField(max_length=255,verbose_name="视频名称")
    video_detail = models.CharField(max_length=255, verbose_name="视频描述")
    video_address = models.CharField(max_length=255, verbose_name="视频地址")
    video_user = models.CharField(max_length=255, verbose_name="用户名")
    video_passwd = models.CharField(max_length=255, verbose_name="密码")

    class Meta():
        verbose_name = "视频表"
        permissions = (
            ('video_view', '视频浏览'),
            ('video_contro', '视频管理')
        )

    def __str__(self):
        return self.video_name


