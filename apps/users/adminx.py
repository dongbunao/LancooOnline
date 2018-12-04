# encoding: utf-8
__author__ = 'dongxiao'

import xadmin
from .models import EmailVerifyRecord
from .models import Banner


# 创建EmailVerifyRecord的管理器，不继承admin，继承object
class EmailVerifyRecordAdmin(object):
    # 配置显示列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 配置搜索字段
    search_fields = ['code', 'email', 'send_type']
    # 过滤器字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 创建Banner的管理器，不继承admin，继承object
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)