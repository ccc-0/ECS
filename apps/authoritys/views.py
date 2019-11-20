from django.db import connection, transaction
from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view,schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from  users.models import *
from  .serializers import *
# from  .filters import *
from  .schema import *

# Create your views here.

#将fetchall转化为字典的函数
def dictfetchall(cursor):
    desc = cursor.description# 得到列名
    print('desc',desc)
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()# ((1,'zs',5),(),())
    ]

class GpuListView(APIView):
    '''1 显用户角色和权限'''
    module_perms = []

    def post(self,request):
        sql='''SELECT new_gp.*,GROUP_CONCAT(users_users_groups.users_id) as users_id,GROUP_CONCAT(users_users.last_name) as users_names
    FROM(
    SELECT auth_group.id,auth_group.`name` as group_name,GROUP_CONCAT(auth_permission.`name`) as permission_names
    FROM auth_group LEFT JOIN auth_group_permissions
    ON auth_group.id = auth_group_permissions.group_id
    LEFT JOIN auth_permission ON auth_permission.id = auth_group_permissions.permission_id
    group by auth_group.id) as new_gp 
    LEFT JOIN users_users_groups
    ON new_gp.id = users_users_groups.group_id
    LEFT JOIN users_users ON users_users.id = users_users_groups.users_id
    GROUP BY new_gp.id'''
        cursor= connection.cursor()
        cursor.execute(sql)
        # result = cursor.fetchall()
        # print(result)
        res=dictfetchall(cursor)
        return Response(data={'data':res,'code':200})


class RoleCreateView(APIView):
    """
    新增角色
    """
    module_perms = ['users.premission_view']
    schema = RoleCreateSchema

    def post(self, request):
        role_name = self.request.data['role']['role_name']
        role_permission = self.request.data['role']['role_permission']
        role_user = self.request.data['role']['role_user']
        role = Group()
        with transaction.atomic():
            try:
                role.name = role_name
                role.save()
            except:
                return Response(data={'code': 400, 'message': '创建失败'})
            role = Group.objects.get(name=role_name)
            if role_permission:
                for permission in role_permission:
                    try:
                        sql = """insert into auth_group_permissions(group_id, permission_id) values({},{})
                        """.format(role.id, permission)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        # role.delete()
                        return Response(data={'code': 400, 'message': '创建失败' + str(e)})
            if role_name:
                for user in role_user:
                    try:
                        sql = """insert into auth_user_groups(group_id, userprofile_id) values ({},{})
                        """.format(role.id, user)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        # role.delete()
                        return Response(data={'code': 400, 'message': '创建失败' + str(e)})
        user = self.request.user
        # logcreate(log_content='新增角色', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '新增成功'})

class PermissionUpdateView(APIView):
    """
    修改权限
    """
    module_perms = ['users.premission_control']
    schema = PermissionUpdateSchema

    def post(self, request):
        role_id = self.request.data['permission']['group_id']
        permission_id = self.request.data['permission']['permission_id']
        with transaction.atomic():
            sql = """delete from auth_group_permissions where group_id = {}
            """.format(role_id)
            cursor = connection.cursor()
            cursor.execute(sql)
            cursor.close()
            if permission_id:
                for permission_id in permission_id:
                    try:
                        sql = """insert into auth_group_permissions(group_id, permission_id) values({},{})
                        """.format(role_id, permission_id)
                        cursor = connection.cursor()
                        cursor.execute(sql)
                        cursor.close()
                    except Exception as e:
                        return Response(data={'code': 400, 'message': '更新失败' + str(e)})
        user = self.request.user
        # logcreate(log_content='修改权限', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '更新成功'})

class RoleDeleteView(APIView):
    """
    删除角色
    """
    module_perms = ['users.premission_control']
    schema = RoleDeleteSchema

    def post(self, request):
        role_id = self.request.query_params.get('role_id')
        with transaction.atomic():
            try:
                sql = """delete from auth_group_permissions where group_id = {}
                        """.format(role_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
                sql = """delete from auth_user_groups where group_id = {}
                        """.format(role_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
                sql = """delete from auth_group where id = {}
                        """.format(role_id)
                cursor = connection.cursor()
                cursor.execute(sql)
                cursor.close()
            except Exception as e:
                return Response(data={'code': 400, 'message': '删除失败' + str(e)})
        user = self.request.user
        # logcreate(log_content='删除角色', log_module='权限管理', user=user)
        return Response(data={'code': 200, 'message': '删除成功'})

