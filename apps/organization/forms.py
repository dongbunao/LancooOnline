# encoding: utf-8
__author__ = 'dongxiao'

import re

from django import forms
from operation.models import UserAsk


# 应为要验证的表单中字段基本和数据库中字段一致，使用modelform
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk # 对应的Model
        fields = ['name', 'mobile', 'course_name'] # 需要验证的字段，对应的Model中字段

    # 对某个字段添加额外验证（除了Model中定义的验证），***必须是 clean_+字段名***
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")

