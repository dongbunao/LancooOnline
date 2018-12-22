# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ActiveForm
from django.contrib.auth.hashers import make_password
from apps.utils.email_send import send_register_email
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


# 用户注册
class RegisterView(View):
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 获取表单传来的值
            user_name = request.POST.get('email', '')
            # 用户已经存在的情况
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':'用户已经存在，请直接登录'})
            pass_word = request.POST.get('password', '')
            # 实例化一个Userprofile对象,把表单传来的值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # password的值需要加密保存
            user_profile.password = make_password(pass_word)

            user_profile.save()

            # 发送激活邮件
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            # 注册邮箱form验证失败
            return  render(request, 'register.html', {'register_form':register_form})

# 用户激活View
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱 验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        #
        active_form = ActiveForm(request.GET)
        # 如果存在记录
        if all_record:
            for record in all_record:
                # 获取对应的邮箱
                email = record.email
                # 查找有相对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功。跳到登录页面
                return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'msg':'您的激活链接无效','active_from':active_form})



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
