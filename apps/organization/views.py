# encoding:utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from organization.models import CourseOrg, CityDict, Teacher
from organization.forms import UserAskForm
from operation.models import UserFavourite
from courses.models import Course
# Create your views here.


# 处理课程机构列表的View
class OrgView(View):
    def get(self, request):
        # 查找所有的课程机构
        all_orgs = CourseOrg.objects.all()
        # 取出所有城市
        all_citys = CityDict.objects.all()
        # 城市筛选,默认空
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 类别筛选（培训机构、学校、个人），默认空
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 授课机构排名,取点击数前三
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        #
        org_nums = all_orgs.count();

        # 按学习人数和课程数排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'learners':
                all_orgs = all_orgs.order_by('-learners')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums') # courses是前端页面参数名，course_nums是数据库中字段名


        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_orgs中取5个出来，每页显示5个
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return  render(request, 'org-list.html', {
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id, # 把city_id传回页面，标记哪个city被选中
            'category':category, # 把category传回页面，标记哪个category被选中
            'hot_orgs':hot_orgs, # 授课机构排名,取点击数前三
            'sort':sort,
        })


# 用户咨询（我要学习）的View
class AddUserAskView(View):
    # 只有post
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 这里是modelform和form的区别
            # 它有model的属性
            # 当commit为true进行真正保存
            user_ask = userask_form.save(commit=True)
            # 这样就不需要把一个一个字段取出来然后存到model的对象中之后save

            # 如果保存成功,返回json字符串,后面content type是告诉浏览器的
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"信息有错"}', content_type='application/json')


# 机构首页
class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]

        # 向前端传 has_fav 说明是否已收藏
        has_fav = False
        # 登录状态才能判断是否收藏
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page, # 前端左侧菜单栏标记哪个选项被active
            'has_fav': has_fav,
        })


# 机构课程
class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'course'
        # 根据org_id取出课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 查询该课程机构下所有课程.
        all_courses = course_org.course_set.all()

        # 向前端传 has_fav 说明是否已收藏
        has_fav = False
        # 登录状态才能判断是否收藏

        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


# 机构描述
class OrgDescView(View):
    """
    机构描述页
    """
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据org_id取出机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 向前端传 has_fav 说明是否已收藏
        has_fav = False
        # 登录状态才能判断是否收藏
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


# 机构讲师列表
class OrgTeacherView(View):
    """
    机构讲师列表页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        # 根据org_id取出课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 查询该课程机构下所有课程.
        all_teacher = course_org.teacher_set.all()

        # 向前端传 has_fav 说明是否已收藏
        has_fav = False
        # 登录状态才能判断是否收藏
        if request.user.is_authenticated:
            if  UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html',{
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


# 用户收藏
class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        # 收藏对象（课程、讲师、机构）的ID
        id = request.POST.get('fav_id', 0)
        # 收藏类别，前端页面ajax请求带来
        type = request.POST.get('fav_type', 0)

        # 判断用户是否登录，只有登录后才能收藏
        if not request.user.is_authenticated:
            # 没有登陆，返回错误提示
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavourite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_records:
            # 记录存在,删除（记录存在说明收藏过了，删除即为取消收藏）
            exist_records.delete()
            if int(type) == 1: # 课程的收藏数-1
                course  = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2: # 机构的收藏数-1
                org  = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(type) == 3: # 教师的收藏数-1
                teacher  = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavourite()
            # 过滤掉 fav_id，fav_type 默认的情况
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:  # 课程的收藏数+1
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:  # 机构的收藏数+1
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                elif int(type) == 3:  # 教师的收藏数+1
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

# 教师详情页面

class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = teacher.course_set.all()
        # 排行榜讲师
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]

        has_fav_teacher = False
        if UserFavourite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavourite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_fav_org = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_course": all_course,
            "rank_teacher": rank_teacher,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org,
        })



