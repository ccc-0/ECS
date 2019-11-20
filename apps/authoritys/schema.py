import coreapi
import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema

token_field = coreapi.Field(
                name="Authorization",
                required=False,
                location="header",
                schema=coreschema.String(),
                description="格式：JWT 值",
        )
TokenSchema = AutoSchema([
                token_field
        ]
)

CreateGroupSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "group_name",
                required=True,
                location="query", #form
                schema=coreschema.String(),
                # schema=coreschema.String(),
                description="角色名称",
            ),
    coreapi.Field(
                "permission_name",
                required=False,
                location="form", #form
                schema=coreschema.String(),
                # schema=coreschema.String(),
                description="权限名称",
            ),
    coreapi.Field(
                "user_name",
                required=False,
                location="form", #form
                schema=coreschema.String(),
                # schema=coreschema.String(),
                description="用户名称",
            ),
])


PermissionUpdateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "permission",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="权限",
            ),
])

UserUpdateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "user",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="用户",
            ),
])

RoleDeleteSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "role_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="角色id",
            ),
])

RoleCreateSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "role",
                required=True,
                location="form",  # from,query,url
                schema=coreschema.Object(),
                # schema=coreschema.String(),
                description="角色",
            ),
])
