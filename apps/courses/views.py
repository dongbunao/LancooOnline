# encoding: utf-8

from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
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
