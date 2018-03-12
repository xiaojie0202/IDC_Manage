from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dc_info.views.commonality import CustomPaginator, add_cabinet_log
from dc_info.utils import handel_excel
import json
import os


# 前端获取机柜信息页面
@login_required
def get_cabinet_info(request, dcname, idcname, *args, **kwargs):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    search_cabinet = request.GET.get('search_cabinet', None)  # 获取用户搜索的机柜信息
    current_page = request.GET.get('page', '1')  # 获取用户点击的页码
    filter = request.GET.get('filter', None)  # 获取过滤信息
    addcabinet = request.GET.get('addcabinet', None)  # 添加机柜的时候跳转此页码会传入此参数
    if search_cabinet:
        cabinet_obj = dc_obj.get(name=dcname).idcinfo_set.get(name=idcname).cabinet_set.filter(number__icontains=search_cabinet)
    else:
        if filter == 'all' or not filter:
            cabinet_obj = dc_obj.get(name=dcname).idcinfo_set.get(name=idcname).cabinet_set.all().order_by('number')  #  获取机柜信息
        else:
            filter = int(filter)
            cabinet_obj = dc_obj.get(name=dcname).idcinfo_set.get(name=idcname).cabinet_set.all().filter(customer=models.Customer.objects.get(pk=filter)).order_by('number')
    if current_page == 'all':
        paginator = CustomPaginator(1, 11, cabinet_obj, cabinet_obj.count())
    else:
        paginator = CustomPaginator(current_page, 11, cabinet_obj, 20)
    try:
        data_list = paginator.page(current_page)  # 分页
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request, 'dc_info/cabinetinfo.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'dcname': dcname, 'idcname': idcname, 'page_list': data_list, 'filter': filter, 'addcabinet': addcabinet})


# 添加机柜
@login_required
def create_cabinet(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    erro = ''
    if request.method == 'GET':
        return render(request, 'dc_info/create_cabinet.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'dcname': dcname, 'idcname': idcname, 'erro': erro})
    elif request.method == 'POST':
        a = ''
        cabinet_num = request.POST.get('number')
        open_date = request.POST.get('open_date')
        customer_id = int(request.POST.get('customer'))
        if models.Cabinet.objects.filter(number=cabinet_num, idc__name=idcname, idc__dc__name=dcname).count() != 0:
            erro = '%s机柜已经存在，无需重复添加' % cabinet_num
            return render(request, 'dc_info/create_cabinet.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'dcname': dcname, 'idcname': idcname, 'erro': erro})
        else:
            idc = models.IDCInfo.objects.get(name=idcname, dc__name=dcname)
            customer = customer_obj.get(pk=customer_id)
            a = models.Cabinet.objects.create(idc=idc, number=cabinet_num, customer=customer, open_date=open_date)
            # 添加机柜操作日志
            add_cabinet_log(request, 1, a)
        return redirect('/cabinet/%s/%s/?addcabinet=%s' % (dcname, idcname, a))


# 删除机柜
@login_required
def delete_cabinet(request):

    if request.method == 'POST':
        idlist = []
        delete_list = ''
        for i in request.POST.values():
            idlist.append(int(i))
        cabinet_queryset = models.Cabinet.objects.filter(pk__in=idlist)
        for a in cabinet_queryset:
            delete_list += '%s,' % a
            # 添加机柜删除日志
            add_cabinet_log(request, 0, a)
            a.delete()
        return HttpResponse(json.dumps({'status': True, 'delete_list': delete_list, 'delete_id': idlist}))


# 批量导入机柜
@login_required
def import_cabinet(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    if request.method ==  'GET':
        return render(request, 'dc_info/import_cabinet.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'dcname': dcname, 'idcname': idcname})
    elif request.method == 'POST':
        cabinet_files = request.FILES.get('cabinet_excel')
        info = {'status': False}
        if cabinet_files:
            file_suffix = os.path.splitext(cabinet_files.name)[1]
            if file_suffix in ('.xls', '.xlsx'):
                try:
                    info = handel_excel.handel_import_cabinet(cabinet_files.file)  # 交给函数出来文件
                except IOError as e:
                    info['erro'] = '文件异常(%s)' % e
                else:
                    if info['status']:
                        info['date'] = []
                        for i in info['cabinet_objlist']:
                            a = models.Cabinet.objects.create(**i)
                            add_cabinet_log(request, 1, a)
                            info['date'].append(a)
            else:
                info['erro'] = '上传文件只能是 .xls 和 .xlsx 格式'
        return render(request, 'dc_info/import_cabinet.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'dcname': dcname, 'idcname': idcname, 'info': info})


# 主页获取机柜操作日志
@login_required
def customet_cabinet_log(request):
    current_page = request.GET.get('page', 1)
    cabinet_number = request.GET.get('cabinet_number')
    customer = request.GET.get('customer', None)
    cabinet_log_obj = models.CabinetLog.objects.all()
    context = {"filter": {}}
    if cabinet_number:
        if customer:
            context["filter"] = {'cabinet_number': cabinet_number, 'customer': customer}
            cabinet_log_obj = cabinet_log_obj.filter(cabinet_number=cabinet_number, customer__name=customer).order_by('handle_date').reverse()
        else:
            context["filter"] = {'cabinet_number': cabinet_number}
            cabinet_log_obj = cabinet_log_obj.filter(cabinet_number=cabinet_number).order_by('handle_date').reverse()
    else:
            if customer:
                context["filter"] = {'customer': customer}
                cabinet_log_obj = cabinet_log_obj.filter(customer__name=customer).order_by('handle_date').reverse()
            else:
                cabinet_log_obj = cabinet_log_obj.order_by('handle_date').reverse()

    paginator = CustomPaginator(current_page, 5, cabinet_log_obj, 11)
    try:
        data_list = paginator.page(current_page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    context['page_list'] = data_list
    return render(request, 'dc_info/customer_cabinet_log.html', context)