# encoding: utf-8
__author__ = 'dongxiao'

from django.urls import path, re_path

from users.views import MyMessageView, MyFavTeacherView, MyFavCourseView, MyFavOrgView, UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView


app_name = 'users'
urlpatterns = [
    # 个人中心
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    # 用户在个人中心页面修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 获取验证码（修改邮箱）
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    path('update/email/', UpdateEmailView.as_view(), name='update_email'),
    # 个人中心我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    # 个人中心我的收藏（机构）
    path('myfav/org', MyFavOrgView.as_view(), name='myfav_org'),
    # 个人中心我的收藏（课程）
    path('myfav/course', MyFavCourseView.as_view(), name='myfav_course'),
    # 个人中心我的收藏（讲师）
    path('myfav/teacher', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 个人中心我的信息
    path('my_message/', MyMessageView.as_view(), name='my_message'),



]