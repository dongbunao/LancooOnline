# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm
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
        # 查询邮箱验证码表中 验证码是否存在
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



# 用户登录View
class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        # 实例化form对象
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



# 忘记密码View
class ForgetPwdView(View):
    def get(self, request):
        # 获取验证码
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})
    def post(self, request):
        # 验证忘记密码页面表单
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码链接（重用注册激活链接）
            send_register_email(email, 'forget')
            # 发送完邮件返回登录页面，提示邮件发送成功
            return render(request, 'login.html', {'msg':'找回密码邮件已发送，请查收'})
        else:
            # 表单验证失败
            return  render(request, 'forgetpwd.html',{'forget_form':forget_form})


# 请求重置密码页面的 get View
class ResetView(View):
    def get(self, request, active_code):
        active_form = ActiveForm(request.POST)
        # 查询邮箱验证码表中 验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                # 把邮箱传递给 密码重置页面
                return render(request, 'password_reset.html', {'email':email})
        else:
            # 邮箱验证码表中 验证码是否存在
            return  render(request, 'forgetpwd.html', {'msg':'重置密码链接无效，请重新请求', 'active_form':active_form})


# 重置密码页面表单提交的 post View
class ModifyPwdView(View):
    def post(self, request):
        # 验证重置密码页面表单
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            # 如果两次密码不一致，返回错误信息
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg':'两次密码不一致', 'email':email})
            # 密码一致
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, 'login.html', {'msg':'密码修改成功，请用新密码登录'})
        else:
            # 重置密码页面表单验证失败
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email':email,'modifypwd_form':modifypwd_form})