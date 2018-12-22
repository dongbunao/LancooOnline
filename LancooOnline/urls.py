"""LancooOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from django.conf.urls import url, include


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # 配置登录页面跳转
    path('login/', LoginView.as_view(), name='login'),
    # 注册url
    path('register', RegisterView.as_view(), name='register'),
    # 验证码url
    path('captcha/', include('captcha.urls')),
    # 请求激活用户url（从激活链接过来的请求）
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    # 点击忘记密码url
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    # 请求重置密码url(从重置链接过来的请求)
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    # 点击重置密码url(重置密码页面提交的表单)
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd')
]
