# encoding: utf-8
__author__ = 'dongxiao'

import xadmin
from .models import UserAsk, CourseComments, UserFavourite, UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['course', 'user', 'comments', 'add_time']
    search_fields = ['course', 'user', 'comments']
    list_filter = ['course', 'user', 'comments', 'add_time']


class UserFavouriteAdmin(object):

    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['course', 'user', 'add_time']
    search_fields = ['course', 'user', 'has_read']
    list_filter = ['course', 'user', 'add_time']


# 把model和管理器进行关联注册
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavourite, UserFavouriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)