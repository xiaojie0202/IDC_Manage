from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dc_info.views.commonality import CustomPaginator
from django.utils import timezone
from dc_info import models


# 前端获取异常信息数据统计页面
def get_abnormal(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    idc_obj = models.DcInfo.objects.get(
        name=dcname).idcinfo_set.filter(
        name=idcname)
    cabinet_obj = models.Cabinet.objects.filter(idc__in=idc_obj)  # 当前机房的所有机柜
    search_abnormal = request.GET.get('search_abnormal', None)  # 获取用户搜索的设备SN号
    current_page = request.GET.get('page', '1')  # 获取用户点击的页码
    schedule = request.GET.get('schedule', None)  # 获取过滤信息
    context = {
        "dc_obj": dc_obj,
        'customer_obj': customer_obj,
        'dcname': dcname,
        'idcname': idcname,
        'filter': {},
        'cabinet_obj': cabinet_obj}
    # 查询当前机房的所有异常告警信息
    abnormal_obj = models.AbnormalInfo.objects.filter(
        equipment__cabinet__idc__in=idc_obj).order_by('-find_time')
    # 点击确认处理按钮的时候传递的get
    handel_abnormal = request.GET.get('handel', None)
    # 点击确认处理按钮
    if handel_abnormal:
        models.AbnormalInfo.objects.filter(
            pk=int(handel_abnormal)).update(
            schedule=1, handel_time=timezone.now())
        return redirect('/abnormal/%s/%s/' % (dcname, idcname))

    if request.method == 'GET':
        # 当有所属异常设备SN
        if search_abnormal:
            abnormal_obj = abnormal_obj.filter(
                equipment__serial_num__icontains=search_abnormal.strip()).order_by('-find_time')
            context['filter']['search_abnormal'] = search_abnormal
        # 显示全部
        if schedule == 'all' or not schedule:
            abnormal_obj = abnormal_obj.order_by('-find_time')
        else:
            schedule = int(schedule)
            abnormal_obj = abnormal_obj.filter(
                schedule=schedule).order_by('find_time').reverse()
            context['filter']['schedule'] = schedule
    # post 增加异常告警信息
    if request.method == 'POST':
        equipment_id = request.POST.get('equipment_id')
        info = request.POST.get('info')
        schedule = request.POST.get('schedule')
        models.AbnormalInfo.objects.create(
            equipment_id=equipment_id,
            info=info,
            schedule=schedule,
            find_time=timezone.now())

    if current_page == 'all':
        paginator = CustomPaginator(1, 11, abnormal_obj, abnormal_obj.count())
    else:
        paginator = CustomPaginator(current_page, 11, abnormal_obj, 20)
    try:
        page_list = paginator.page(current_page)  # 分页
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)
    context['page_list'] = page_list
    return render(request, 'dc_info/abnormal.html', context)
