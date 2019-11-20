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

SceneListSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "scene",
                required=True,
                location="query", #form
                schema=coreschema.Integer(),
                # schema=coreschema.String(),
                description="场景ID",
            ),
])

SceneFireHistorySchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "start_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="结束时间",
            ),
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
])

SceneEnvironmentHistorySchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "start_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="结束时间",
            ),
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
    coreapi.Field(
                "scene_env_device",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="环境设备名称",
            ),
])

SceneEnvironmentAlarmSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "start_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_time",
                required=False,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="结束时间",
            ),
    coreapi.Field(
                "scene_id",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.Integer,
                # schema=coreschema.String(),
                description="场景id",
            ),
    coreapi.Field(
                "scene_env_device",
                required=True,
                location="query",  # from,query,url
                schema=coreschema.String,
                # schema=coreschema.String(),
                description="环境设备名称",
            ),
])

