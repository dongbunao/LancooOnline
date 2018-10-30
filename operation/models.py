# coding:utf-8
from django.db import models
from datetime import datetime

from users.models import UserProfile
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


# 用户对于课程的评论
class CourseComments(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'用户')
    comments = models.CharField(max_length=300, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


# 用户对于 课程 机构 讲师的收藏
class UserFavourite(models.Model):
    TYPE_CHOICE = (
        (1, u'课程'),
        (2, u'机构'),
        (3, u'讲师')
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0)
    fav_type = models.IntegerField(choices=TYPE_CHOICE, default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # 0 代表所有用户， 不为0就是发给用户的ID
    user = models.IntegerField(default=0, verbose_name=u'接收用户')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    # 是否已读
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


# 用户课程表
class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    user = models.IntegerField(default=0, verbose_name=u'用户')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name