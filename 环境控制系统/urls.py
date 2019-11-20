"""环境控制系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url,include
from django.contrib import admin
import rest_framework.authtoken.views
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='环境控制系统 API')

urlpatterns = [
    path(r'admin/', admin.site.urls),

    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', obtain_jwt_token),  #jwt验证方式
    url(r'^api/', schema_view),
    # url(r'^demo_app/', include('DemoApp.urls', namespace='demo_app')),

    path(r'users/',include('users.urls',namespace='users')),  #users
    path(r'logs/',include('logs.urls',namespace='logs')),  #logs
    path(r'videos/',include('videos.urls',namespace='videos')),  #videos
    path(r'door_limits/',include('door_limits.urls',namespace='door_limits')),  #door_limits
    path(r'scenes/',include('scenes.urls',namespace='scenes')),  #scenes
    path(r'alarms/',include('alert.urls',namespace='alarms')),  #alarms
    path(r'authoritys/',include('authoritys.urls',namespace='authoritys')),  #authoritys

]
