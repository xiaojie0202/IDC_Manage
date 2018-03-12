from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dc_info.views.commonality import CustomPaginator
from dc_info.utils import handel_excel
from dc_info import model_forms
from django.db.models import Q
from django.db.models import F
import json
import os


# 前端获取库存信息
@login_required
def get_inventory(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    current_page = request.GET.get('page', 1)
    filter = request.GET.get('filter', None)  # 获取过滤信息
    addinfo = request.GET.get('add', None)  # 添加库存的时候跳转过来并传递add参数
    search_inventory = request.GET.get('search')
    context = {
        "dc_obj": dc_obj,
        'customer_obj': customer_obj,
        'dcname': dcname,
        'idcname': idcname,
        'add': addinfo}
    inventory_queryset = models.DcInfo.objects.get(
        name=dcname).idcinfo_set.get(
        name=idcname).inventory_set
    if search_inventory:
        inventory_queryset = inventory_queryset.filter(Q(sn__icontains=search_inventory) | Q(
            post_number__icontains=search_inventory)).order_by('id')
    else:
        if filter == 'all' or not filter:
            inventory_queryset = inventory_queryset.all().order_by('id')
        else:
            filter = int(filter)
            inventory_queryset = inventory_queryset.filter(
                customer=customer_obj.get(pk=filter)).order_by('id')

    if current_page == 'all':
        paginator = CustomPaginator(
            1, 11, inventory_queryset, inventory_queryset.count())
    else:
        paginator = CustomPaginator(current_page, 11, inventory_queryset, 20)
    try:
        data_list = paginator.page(current_page)  # 分页
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    context['page_list'] = data_list
    context['filter'] = filter
    return render(request, 'dc_info/inventoryinfo.html', context)


# 删除库存信息
@login_required
def delete_inventory(request):
    if request.method == 'POST':
        idlist = []
        for i in request.POST.values():
            idlist.append(int(i))
        models.Inventory.objects.filter(pk__in=idlist).delete()
        return HttpResponse(json.dumps({'status': True, 'delete_id': idlist}))


# 增减库存数量
def update_inventory_count(request, operation):
    if request.method == 'POST':
        inventory_id = request.POST.get('inventory_id')
        if operation == 'add':
            models.Inventory.objects.filter(
                pk=int(inventory_id)).update(
                count=F('count') + 1)
        elif operation == 'minus':
            models.Inventory.objects.filter(
                pk=int(inventory_id)).update(
                count=F('count') - 1)
        return HttpResponse(json.dumps({'status': True}))


# 增加库存信息
@login_required
def add_inventory(request, dcname, idcname):
    context = {}
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    context['dc_obj'] = dc_obj
    context['customer_obj'] = customer_obj
    context['dcname'] = dcname
    context['idcname'] = idcname
    if request.method == 'GET':
        inventory_form = model_forms.InventoryForms(
            initial={
                'idc': models.DcInfo.objects.get(
                    name=dcname).idcinfo_set.get(
                    name=idcname)})
        context['inventory_form'] = inventory_form
        return render(request, 'dc_info/edit_inventory.html', context)
    if request.method == 'POST':
        inventory_form = model_forms.InventoryForms(request.POST)
        context['inventory_form'] = inventory_form
        if inventory_form.is_valid():
            obj = inventory_form.save()
            return redirect(
                '/inventory/%s/%s/?add=%s' %
                (dcname, idcname, obj))
        else:
            return render(request, 'dc_info/edit_inventory.html', context)


# 编辑库存信息
@login_required
def edit_inventory(request, dcname, idcname, inventory_id):
    context = {}
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    context['dc_obj'] = dc_obj
    context['customer_obj'] = customer_obj
    context['dcname'] = dcname
    context['idcname'] = idcname
    if request.method == 'GET':
        inventory_form = model_forms.InventoryForms(
            instance=models.Inventory.objects.get(
                pk=int(inventory_id)))
        context['inventory_form'] = inventory_form
        return render(request, 'dc_info/edit_inventory.html', context)
    if request.method == 'POST':
        inventory_form = model_forms.InventoryForms(
            request.POST, instance=models.Inventory.objects.get(
                pk=int(inventory_id)))
        context['inventory_form'] = inventory_form
        if inventory_form.is_valid():
            obj = inventory_form.save()
            return redirect(
                '/inventory/%s/%s/?add=%s' %
                (dcname, idcname, obj))
        else:
            return render(request, 'dc_info/edit_inventory.html', context)


# 批量导入库存信息
@login_required
def bulk_import_inventory(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    context = {
        'dc_obj': dc_obj,
        'customer_obj': customer_obj,
        'dcname': dcname,
        'idcname': idcname}

    if request.method == 'GET':
        return render(request, 'dc_info/import_inventory.html', context)
    if request.method == 'POST':
        info = {}
        inventory_excel = request.FILES.get('inventory_excel')
        if inventory_excel:
            file_suffix = os.path.splitext(inventory_excel.name)[1]
            if file_suffix in ('.xls', '.xlsx'):
                info = handel_excel.handel_import_inventory(
                    inventory_excel.file, dcname, idcname)
            else:
                info['status'] = False
                info['erro'] = '上传文件只能是 .xls 和 .xlsx 格式'
            context['info'] = info
            return render(request, 'dc_info/import_inventory.html', context)
