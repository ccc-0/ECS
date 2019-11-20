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

AlarmStatisticsSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "stat_addtime",
                required=True,
                location="query", #form
                # schema=coreschema.Integer(),
                schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_addtime",
                required=True,
                location="query", #form
                # schema=coreschema.Integer(),
                schema=coreschema.String(),
                description="结束时间",
            ),
])

AlarmTypePrecentSchema = AutoSchema([
    # token_field,
    coreapi.Field(
                "stat_addtime",
                required=False,
                location="query", #form
                # schema=coreschema.Integer(),
                schema=coreschema.String(),
                description="开始时间",
            ),
    coreapi.Field(
                "end_addtime",
                required=False,
                location="query", #form
                # schema=coreschema.Integer(),
                schema=coreschema.String(),
                description="结束时间",
            ),
])