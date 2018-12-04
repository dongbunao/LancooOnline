# encoding: utf-8
__author__ = 'dongxiao'

import xadmin
from .models import CityDict, CourseOrg, Teacher


# 机构所属城市的管理器
class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']

# 把model和管理器进行关联注册
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)