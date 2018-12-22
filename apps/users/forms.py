# encoding: utf-8
__author__ = 'dongxiao'

from django import forms
from captcha.fields import CaptchaField

# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能空，最小长度 最大长度
    username = forms.CharField(required=True, max_length=20, min_length=3)
    password = forms.CharField(required=True, max_length=20, min_length=3)

# 验证码form && 注册表单from
class RegisterForm(forms.Form):
    # 这里email和前端name一致
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


# 验证码激活
class ActiveForm(forms.Form):
    # 这里是email，和前端页面的name一致
    email = forms.CharField(required=True)
    # 用用验证码，自定义错误输出（key必须和异常一致）
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})