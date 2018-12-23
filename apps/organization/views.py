# encoding:utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm

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

