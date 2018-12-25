# encoding: utf-8
__author__ = 'dongxiao'

from django.urls import path, re_path
from django.views.generic import TemplateView
from courses.views import CourseListView, CourseDetailView

app_name = 'course'
urlpatterns = [
    # 课程列表
    path('list/', CourseListView.as_view(), name='list'),
    # 课程详情页
    re_path('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),

]
