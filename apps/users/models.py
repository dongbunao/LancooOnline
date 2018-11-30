# conding=utf-8
from django.db import models
from datetime import datetime


from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    # 性别选择器
    GENDER_CHOICES = (
        ('male', u'男'),
        ('female', u'女')
    )

    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称',default='')
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        verbose_name=u'性别',
        choices=GENDER_CHOICES,
        default='female'
    )
    address = models.CharField(max_length=100, verbose_name=u'地址', default='')
    mobile = models.CharField(max_length=11, verbose_name=u'手机号', null=True, blank=True)
    # 头像 默认使用default.png
    image = models.ImageField(max_length=100, verbose_name=u'头像', upload_to='image/%Y/%m', default=u'image/default.png')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    # 重载 str 方法，打印实例会打印username，username为继承自abstractuser
    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', u'注册'),
        ('forget', u'找回密码')
    )
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, verbose_name=u'发送类型', choices=SEND_CHOICES)
    send_time = models.DateTimeField( verbose_name=u'发送时间',default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name
    # 重载 str 方法，后台不再直接显示object
    def __str__(self):
        return '{0} ({1})'.format(self.code, self.email)

class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name=u'轮播图')
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    # 重载 str 方法，后台不再直接显示object
    def __str__(self):
        return self.title