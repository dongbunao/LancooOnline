# conding:utf-8
from django.db import models
from datetime import  datetime

from organization.models import CourseOrg
# Create your models here.

class Course(models.Model):
    DEGREE_CHOICE = (
        ('cj', u'初级'),
        ('zj', u'中级'),
        ('gj', u'高级')
    )
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')

    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(max_length=2, choices=DEGREE_CHOICE, verbose_name=u'难度等级')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', verbose_name=u'封面图')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    tag = models.CharField(default='', max_length=15, verbose_name='课程标签')
    category = models.CharField(default='', max_length=20, verbose_name='课程类别')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取课程章节
    def get_lesson_nums(self):
        return  self.lesson_set.count()

    # 获取学习了这门课程的用户
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]


class Lesson(models.Model):
    # django2.X 外键必须要声明 on_delete 属性
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=u'章节')
    name = models.CharField(max_length=50, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'名称')
    download = models.FileField(
        upload_to='course/resource/%Y/%m',
        verbose_name=u'资源文件',
        max_length=50
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name