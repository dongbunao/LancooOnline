# encoding: utf-8
__author__ = 'dongxiao'

from random import  Random
from users.models import EmailVerifyRecord
from django.core.mail import  send_mail
from LancooOnline.settings import EMAIL_FROM, ALI_HOST


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]

    return str


# 发送注册激活邮件
def send_register_email(email, send_type):
    # 实例化一个EmailVerifyRecoder对象
    email_record = EmailVerifyRecord()
    # 生成一个随机字符串code放进链接
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    # 发送之前先保存到数据库，到时候查询连接是否存在
    email_record.save()

    # 定义邮件内容
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '蓝鸽在线教育网 注册激活链接'
        email_body = '请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        # 使用Django内置函数发送邮件。四个参数：主题，邮件内容，发送者，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '蓝鸽在线教育网 找回密码链接'
        email_body = '请点击下面链接找回密码：http://{0}:8000/reset/{1}'.format(ALI_HOST, code)

        # 使用Django内置函数发送邮件。四个参数：主题，邮件内容，发送者，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '蓝鸽在线教育网 找回密码链接'
        email_body = '您正在修改邮箱，验证码为{0}'.format(code)

        # 使用Django内置函数发送邮件。四个参数：主题，邮件内容，发送者，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
