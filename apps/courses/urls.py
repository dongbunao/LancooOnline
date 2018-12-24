# encoding: utf-8
__author__ = 'dongxiao'

from django.urls import path, re_path
from django.views.generic import TemplateView
from courses.views import CourseListView

app_name = 'course'
urlpatterns = [
    # 课程列表
    path('list/', CourseListView.as_view(), name='list'),

]
