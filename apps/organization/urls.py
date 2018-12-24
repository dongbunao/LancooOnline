# encoding: utf-8
__author__ = 'dongxiao'

from django.urls import path, re_path
from organization.views import OrgView
from organization.views import AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView


app_name = 'organization'
urlpatterns = [
    # 机构首页
    path('list/', OrgView.as_view(), name='org_list'),
    # 添加我要学习
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    # 机构home页面，取纯数字
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),
    # 机构课程页面
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),
    # 机构介绍页面
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),
    # 机构讲师页面
    re_path('teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),
    # 收藏
    path('add_fav/', AddFavView.as_view(), name='add_fav'),

]