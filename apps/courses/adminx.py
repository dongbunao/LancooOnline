# encoding: utf-8
__author__ = 'dongxiao'

import xadmin
from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']


class LessionAdmmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # __name 意思是使用外键中的name字段
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fileds = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 把管理器和model进行关联注册
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessionAdmmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)