from rest_framework.permissions import BasePermission

class ModulePermission(BasePermission):
    '''
    ModulePermission, 检查一个用户是否有对应某些module以及object的权限
    APIView需要实现module_perms属性m_object属性:
        type: list；obj
        example: module_perms=['information.information', 'school.school'] # app_label.codename
    权限说明:
        1. is_superuser有超级权限
        2. 权限列表请在api.models.Permission的class Meta中添加(请不要用数据库直接添加)
        3. 只要用户有module_perms的一条符合结果即认为有权限, 所以module_perms是or的意思
    '''

    authenticated_users_only = True# 通过身份验证的用户

    def has_perms(self, request, perms):
        #自定义权限验证修改这
        # for perm in perms:
        #     if request.user.has_perm(perm,obj):
        #         return True
        # return False

        user_perms = request.user.get_all_permissions()#用户所有权限
        print(user_perms)
        for perm in perms:
            if perm in user_perms:
                return True
        return False

    def get_module_perms(self, view):


        return ['{}'.format(perm) for perm in view.module_perms]# view.module_perms通过类名拿到某个属性
        # return ['api.{}'.format(perm) for perm in view.module_perms]

    def has_permission(self, request, view):
        '''
        is_superuser用户有上帝权限，测试的时候注意账号
        '''
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        # is_superuser用户有上帝权限
        if request.user.is_superuser:
            return True

        
        return (
                request.user and
                (request.user.is_authenticated or not self.authenticated_users_only) and
                self.has_perms(request, self.get_module_perms(view))
                # request.user and
                # (request.user.is_authenticated() or not self.authenticated_users_only) and
                # self.has_perms(request, self.get_module_perms(view))
        )


