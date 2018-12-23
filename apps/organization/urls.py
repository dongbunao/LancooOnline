# encoding: utf-8
__author__ = 'dongxiao'

from django.urls import path
from organization.views import OrgView
from organization.views import AddUserAskView


app_name = 'organization'
urlpatterns = [
    # 课程机构首页
    path('list/', OrgView.as_view(), name='org_list'),
    # 添加我要学习
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),

]