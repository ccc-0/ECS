from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Users(AbstractUser):
    # user_id = models.IntegerField(primary_key=True,verbose_name="用户id")
    # user_addtime = models.DateTimeField(verbose_name="添加时间")
    # user_name = models.CharField(max_length=255, verbose_name="用户姓名")
    # user_account = models.CharField(max_length=255,verbose_name="用户账号")
    user_number = models.CharField(max_length=255,verbose_name="用户工号")
    user_tel = models.CharField(max_length=20,verbose_name="用户电话")
    GENDERS=((1,'男'),(2,'女'))
    user_gender=models.IntegerField(choices=GENDERS,default=1,verbose_name='用户性别')
    # user_logtime= models.DateTimeField(verbose_name="最新登陆时间")
    # USER_STATUS=((1,'可用'),(2,'禁用'))
    # user_statu = models.IntegerField(choices=USER_STATUS,verbose_name='用户状态')
    user_detail = models.CharField(max_length=255,verbose_name="用户描述信息")
    user_picture=models.CharField(max_length=255,verbose_name="用户头像")

    class Meta():
        verbose_name = "用户表"
        permissions = (
            ('user_view', '用户浏览'),
            ('user_contro', '用户管理')
        )

    # def __str__(self):
        # return self.username

# class Role(Group):
#     role_id =models.IntegerField(primary_key=True,verbose_name='角色id')
#     role_addtime = models.DateTimeField(verbose_name='角色添加时间')
#     role_name = models.CharField(max_length=255,verbose_name='角色名称')
#     role_detail = models.CharField(max_length=255,verbose_name='角色描述')
#
#     class Meta():
#         verbose_name = "角色表"
#
#     def __str__(self):
#         return self.role_name

# class User_role(models.Model):
#     user_role_id = models.IntegerField(primary_key=True,verbose_name='用户角色id')
#     user_role_addtime = models.DateTimeField(verbose_name="添加时间")
#     user_id=models.ForeignKey(Users,on_delete=models.CASCADE)
#     role_id =models.ForeignKey(Role,on_delete=models.CASCADE)
#
#     class Meta():
#         verbose_name = "用户的角色表(用户和角色的桥表)"
#
#     def __str__(self):
#         return self.user_role_id

# class Authority(Permission):
#     authority_id = models.IntegerField(primary_key=True,verbose_name="权限id")
#     authority_addtime = models.DateTimeField(verbose_name="权限添加时间")
#     authority_name = models.CharField(max_length=255,verbose_name="权限名称")
#     authority_num = models.IntegerField(verbose_name="权限类型/编号")
#     authority_realtion = models.IntegerField(verbose_name="权限关系")
#
#     class Meta():
#         verbose_name = "权限表"
#
#     def __str__(self):
#         return self.authority_name

# class Role_authority(models.Model):
#     role_authority_id = models.IntegerField(primary_key=True,verbose_name="角色权限id")
#     role_authority_addtime = models.DateTimeField(verbose_name="添加时间")
#     role_id = models.ForeignKey(Role,on_delete=models.CASCADE)
#     authority_id = models.ForeignKey(Authority,on_delete=models.CASCADE)
#
#     class Meta():
#         verbose_name = "角色的权限表(角色和权限的桥表)"
#
#     def __str__(self):
#         return self.role_authority_id

