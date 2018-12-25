# encoding: utf-8

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
from operation.models import UserFavourite
# Create your views here.


# 课程列表
class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all()

        # 按学习人数和热度排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')  # hot是前端页面参数名，click_nums是数据库中字段名

        #  热门课程
        hot_courses = Course.objects.all().order_by('-students')[:3]

        # 对课程列表进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从all_course中取5个出来，每页显示5个
        p = Paginator(all_course, 5, request=request)
        all_course = p.page(page)

        return render(request, 'course-list.html', {
            'all_course':all_course,
            'sort':sort,
            'hot_courses':hot_courses,
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程点击数 +1
        course.click_nums += 1
        course.save()

        # 相关课程    tag相同的课程
        tag = course.tag
        if tag:
            # 需要从1开始，过滤掉自己
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []

        # 收藏课程
        has_fav_course = False
        has_fav_org = False

        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavourite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavourite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })
