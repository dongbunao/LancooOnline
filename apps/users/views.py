# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm
# Create your views here.

# 实现用户名和邮箱都可以登录
# 继承ModelBackend，重写它的authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None;

# 基于类的登录方法
class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        #
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # authenticate() 验证成功返回user，验证失败返回None
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # login(request, user) django 自身的方法，原理待研究
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})
