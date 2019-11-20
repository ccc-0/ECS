from django.db import models
from users.models import Users
from scenes.models import Scene
from datetime import datetime
# Create your models here.

class Door_approval(models.Model):
    door_addtime  = models.DateTimeField(default=datetime.now,verbose_name='门禁申请时间')
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    door_start = models.DateTimeField(default=datetime.now,verbose_name='申请开始时间')
    door_end = models.DateTimeField(null=True,verbose_name='申请结束时间')
    door_follow =models.CharField(max_length=255,null=True,verbose_name='随行人员')
    door_follownum =models.IntegerField(default=0,verbose_name='随行人数')
    door_detail=models.CharField(max_length=255,null=True,verbose_name='申请说明')
    DOOR_STATUS = (
        (1,'待审核'),(2,'已通过'),(3,'已拒绝')
    )
    door_status=models.IntegerField(choices=DOOR_STATUS,default=1,verbose_name='申请状态')
    door_user = models.IntegerField(verbose_name='审核人',null=True)
    door_audittime =models.DateTimeField(null=True,verbose_name='审批时间')
    door_feedback=models.CharField(max_length=255,null=True,verbose_name='审批反馈')
    scene_id =models.ForeignKey(Scene,on_delete=models.CASCADE)

    class Meta():
        verbose_name = "门禁审批表"
        permissions = (
            ('door_view', '门禁浏览'),
            ('door_audit', '门禁审批')
        )

