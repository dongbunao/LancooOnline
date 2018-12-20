# encoding: utf-8
__author__ = 'dongxiao'

from django import forms

# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能空，最小长度 最大长度
    username = forms.CharField(required=True, max_length=20, min_length=3)
    password = forms.CharField(required=True, max_length=20, min_length=3)