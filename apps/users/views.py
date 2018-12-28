# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from users.models import UserProfile, EmailVerifyRecord
from users.forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm, UploadImageFrom, UserInfoForm
from utils.email_send import send_register_email
from operation.models import UserCourse, UserFavourite, UserMessage
from courses.models import Course
from organization.models import CourseOrg, Teacher
# Create your views here.


# 实现用户名和邮箱都可以登录
# 继承ModelBackend，重写它的authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None;


# 用户注册
class RegisterView(View):
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 获取表单传来的值
            user_name = request.POST.get('email', '')
            # 用户已经存在的情况
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form':register_form, 'msg':'用户已经存在，请直接登录'})
            pass_word = request.POST.get('password', '')
            # 实例化一个Userprofile对象,把表单传来的值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # password的值需要加密保存
            user_profile.password = make_password(pass_word)

            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册蓝鸽在线教育! --系统自动消息"
            user_message.save()

            # 发送激活邮件
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            # 注册邮箱form验证失败
            return  render(request, 'register.html', {'register_form':register_form})

# 用户激活View
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证码表中 验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        #
        active_form = ActiveForm(request.GET)
        # 如果存在记录
        if all_record:
            for record in all_record:
                # 获取对应的邮箱
                email = record.email
                # 查找有相对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功。跳到登录页面
                return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'msg':'您的激活链接无效','active_from':active_form})



# 用户登录View
class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        # 实例化form对象
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # authenticate() 验证成功返回user，验证失败返回None
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 可以对用户角色进行限制（超级管理员，学校，教师，普通用户）

                # login(request, user) django 自身的方法，原理待研究
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})



# 忘记密码View
class ForgetPwdView(View):
    def get(self, request):
        # 获取验证码
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})
    def post(self, request):
        # 验证忘记密码页面表单
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            # 发送找回密码链接（重用注册激活链接）
            send_register_email(email, 'forget')
            # 发送完邮件返回登录页面，提示邮件发送成功
            return render(request, 'login.html', {'msg':'找回密码邮件已发送，请查收'})
        else:
            # 表单验证失败
            return  render(request, 'forgetpwd.html',{'forget_form':forget_form})


# 请求重置密码页面的 get View
class ResetView(View):
    def get(self, request, active_code):
        active_form = ActiveForm(request.POST)
        # 查询邮箱验证码表中 验证码是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                # 把邮箱传递给 密码重置页面
                return render(request, 'password_reset.html', {'email':email})
        else:
            # 邮箱验证码表中 验证码是否存在
            return  render(request, 'forgetpwd.html', {'msg':'重置密码链接无效，请重新请求', 'active_form':active_form})


# 重置密码页面表单提交的 post View
class ModifyPwdView(View):
    def post(self, request):
        # 验证重置密码页面表单
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            # 如果两次密码不一致，返回错误信息
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg':'两次密码不一致', 'email':email})
            # 密码一致
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request, 'login.html', {'msg':'密码修改成功，请用新密码登录'})
        else:
            # 重置密码页面表单验证失败
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email':email,'modifypwd_form':modifypwd_form})


# 用户个人信息View
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, 'usercenter-info.html', {})
    def post(self, request):
        # 需要知名instance，不然不知道给谁修改
        user_info_from = UserInfoForm(request.POST, instance=request.user)
        if user_info_from.is_valid():
            user_info_from.save()


# 用户上传图片的view：用于修改头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        # 此时上传的文件已经被保存到imageform中了
        image_from = UploadImageFrom(request.POST, request.FILES, instance=request.user)
        if image_from.is_valid():
            image_from.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


# 在个人中心修改用户密码
class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)

        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"填写有误！"}', content_type='application/json')


# 发送验证码（修改邮箱）
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        # 取出邮箱
        email = request.GET.get('email', '')

        # 验证邮箱是否被注册过
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经被注册！"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


# 个人中心修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.GET.get('email', '')
        code = request.GET.get('code', '')

        # 判断邮箱验证码表中有没有发送记录
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


# 个人中心我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        # 用户课程表，取出含有该用户的所有课程
        user_courses = UserCourse.objects.filter(user=request.user)
        # 取出所有记录中的 课程id 字段
        course_ids = [user_course.course_id for user_course in user_courses]
        mycourse = Course.objects.filter(id__in=course_ids)

        return  render(request, 'usercenter-mycourse.html', {
            'mycourse':mycourse,
        })


# 个人中心 我的收藏(机构)
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavourite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list,
        })


# 个人中心 我的收藏(公开课)
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavourite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
        })


# 个人中心 我的收藏(公开课)
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavourite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list,
        })


# 个人中心 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人中心消息页面，清空未读消息记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 分页 （异常：'Page' object is not iterable 待解决 2018.12.28）
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4)
        massages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'massages':massages,
        })
