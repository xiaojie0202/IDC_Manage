from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory
from dc_info.utils import handel_excel
from django.db.utils import IntegrityError
from dc_info import model_forms
from django.db.models import Q
from dc_info.views.commonality import CustomPaginator, add_equipment_log

import json
import os


# 前端获取设备信息页面
@login_required
def get_equipmen_info(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    cabinet_queryset = models.DcInfo.objects.get(
        name=dcname).idcinfo_set.get(
        name=idcname).cabinet_set.all()
    current_page = request.GET.get('page', 1)  # 获取用户点击的页码
    cabinet_id = request.GET.get('cabinet_id')
    customer_id = request.GET.get('customer_id')
    search_cabinet = request.GET.get('search_cabinet')
    addequipment = request.GET.get('addequipment', None)
    condition = {}
    if not search_cabinet:
        if cabinet_id:
            condition['cabinet_id'] = int(cabinet_id)
        if customer_id:
            condition['customer_id'] = int(customer_id)
        equipmen_obj = models.Equipmen.objects.filter(
            cabinet__in=cabinet_queryset, **condition).order_by('cabinet')
    else:
        search_equipment = search_cabinet.strip()
        equipmen_obj = models.Equipmen.objects.filter(
            cabinet__in=cabinet_queryset).order_by('cabinet').filter(
            Q(
                ipaddress__ipaddre=search_equipment) | Q(
                serial_num__icontains=search_equipment) | Q(
                    node__icontains=search_equipment))
    if current_page == 'all':
        paginator = CustomPaginator(1, 11, equipmen_obj, equipmen_obj.count())
    else:
        paginator = CustomPaginator(current_page, 11, equipmen_obj, 30)

    try:
        data_list = paginator.page(current_page)  # 分页
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request,
                  'dc_info/equipmeninfo.html',
                  {"dc_obj": dc_obj,
                   'customer_obj': customer_obj,
                   'dcname': dcname,
                   'idcname': idcname,
                   'page_list': data_list,
                   'cabinet_queryset': cabinet_queryset,
                   'filter': condition,
                   'addequipment': addequipment})


# 删除设备
@login_required
def delete_equipment(request):
    if request.method == 'POST':
        idlist = []
        delete_list = ''
        for i in request.POST.values():
            idlist.append(int(i))
        equipment_qyeryset = models.Equipmen.objects.filter(pk__in=idlist)
        for equipment_obj in equipment_qyeryset:
            delete_list += '%s,' % equipment_obj
            # 添加设备删除日志
            add_equipment_log(request, 0, equipment_obj)
            equipment_obj.delete()
        return HttpResponse(json.dumps(
            {'status': True, 'delete_list': delete_list, 'delete_id': idlist}))


# 增加设备信息
@login_required
def create_equipment(request, dcname, idcname):
    context = {}
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    IpAddressFormSet = modelformset_factory(
        model=models.IpAddress,
        form=model_forms.IpAddressForms)
    PortInfoFormSet = modelformset_factory(
        model=models.PortInfo,
        form=model_forms.PortInfoForms)
    context['dc_obj'] = dc_obj
    context['customer_obj'] = customer_obj
    context['dcname'] = dcname
    context['idcname'] = idcname
    if request.method == 'GET':
        cabinet_chuices = models.Cabinet.objects.filter(
            idc__name=idcname).values_list('id', 'number')
        equipment_form = model_forms.EquipmentForms(cabinet_chuices)
        ipaddr_form = IpAddressFormSet(
            queryset=models.IpAddress.objects.none(), prefix='ip')
        portinfo_form = PortInfoFormSet(
            queryset=models.PortInfo.objects.none(), prefix='port')
        context['equipment_form'] = equipment_form
        context['ipaddr_form'] = ipaddr_form
        context['portinfo_form'] = portinfo_form
        return render(request, 'dc_info/create_equipment.html', context)
    elif request.method == 'POST':
        cabinet_chuices = models.Cabinet.objects.filter(
            idc__name=idcname).values_list('id', 'number')
        equipment_form = model_forms.EquipmentForms(
            cabinet_chuices, request.POST)
        ipaddr_form = IpAddressFormSet(request.POST, prefix='ip')
        portinfo_form = PortInfoFormSet(request.POST, prefix='port')
        context['equipment_form'] = equipment_form
        context['ipaddr_form'] = ipaddr_form
        context['portinfo_form'] = portinfo_form
        if equipment_form.is_valid() and ipaddr_form.is_valid() and portinfo_form.is_valid():
            eq_obj = equipment_form.save()
            ip_obj = ipaddr_form.save(commit=False)
            for ip in ip_obj:
                ip.equipmen = eq_obj
                ip.save()
            port_obj = portinfo_form.save(commit=False)
            for port in port_obj:
                port.self_equipment = eq_obj
                port.save()
            add_equipment_log(request, 1, eq_obj)

            return redirect(
                '/equipmen/%s/%s/?addequipment=%s' %
                (dcname, idcname, eq_obj))
        else:
            return render(request, 'dc_info/create_equipment.html', context)


# 前端批量导入设备信息
@login_required
def import_equipment(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    if request.method == 'GET':
        return render(request,
                      'dc_info/import_equipment.html',
                      {"dc_obj": dc_obj,
                       'customer_obj': customer_obj,
                       'dcname': dcname,
                       'idcname': idcname})
    elif request.method == 'POST':
        equipment_info = {'status': True}
        equipment_file = request.FILES.get('equipment_excel')
        if equipment_file:
            file_suffix = os.path.splitext(equipment_file.name)[1]
            if file_suffix in ('.xls', '.xlsx'):
                equipment_list = []
                try:
                    equipment_dict, erroinfo = handel_excel.handel_import_equipment(
                        equipment_file.file, dcname, idcname)  # 交给函数出来文件
                except Exception as e:
                    equipment_info['status'] = False
                    equipment_info['erro'] = 'EXCEL格式不正确,(%s)' % e
                else:
                    if erroinfo['status']:
                        for i in equipment_dict:
                            ipaddress_set = i.pop('ipaddrss_set')
                            portinfo = i.pop('portinfo_set')
                            try:
                                a = models.Equipmen.objects.create(**i)
                            except IntegrityError as e:
                                equipment_info['status'] = False
                                equipment_info['erro'] = '%s-设备已经存在，无需添加:%s' % (
                                    i.get('serial_num'), e)
                                break
                            else:
                                equipment_list.append(a)
                            if ipaddress_set:
                                for ipaddre in ipaddress_set:
                                    ipaddre['equipmen'] = a
                                    try:
                                        models.IpAddress.objects.create(
                                            **ipaddre)
                                    except Exception as e:
                                        equipment_info['status'] = False
                                        equipment_info['erro'] = 'IP地址不能为空%s' % ipaddre
                                        break
                            if portinfo:
                                for port in portinfo:
                                    port['self_equipment'] = a
                                    try:
                                        up_equipment = models.Equipmen.objects.get(
                                            serial_num=port['up_equipment'])
                                    except Exception as e:
                                        equipment_info['status'] = False
                                        equipment_info['erro'] = '%s-上联设备不存在:%s' % (
                                            port.get('up_equipment'), e)
                                        break
                                    else:
                                        port['up_equipment'] = up_equipment
                                        models.PortInfo.objects.create(**port)
                        if equipment_info['status']:
                            for obj in equipment_list:
                                add_equipment_log(request, 1, obj)
                        else:
                            for obj in equipment_list:
                                obj.delete()
                        equipment_info['equipment_obj'] = equipment_list
                    else:
                        equipment_info['status'] = False
                        equipment_info['erro'] = erroinfo['erro']

        return render(request,
                      'dc_info/import_equipment.html',
                      {"dc_obj": dc_obj,
                       'customer_obj': customer_obj,
                       'dcname': dcname,
                       'idcname': idcname,
                       'equipment_info': equipment_info})


# 编辑设备信息
@login_required
def edit_equipment(request, dcname, idcname, equipment_id):
    context = {}
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    # IP地址的Formset表单
    IpAddressFormSet = modelformset_factory(
        model=models.IpAddress,
        form=model_forms.IpAddressForms,
        can_delete=True)
    # 端口信息的Formset表单
    PortInfoFormSet = modelformset_factory(
        model=models.PortInfo,
        form=model_forms.PortInfoForms,
        can_delete=True)
    context['dc_obj'] = dc_obj
    context['customer_obj'] = customer_obj
    context['dcname'] = dcname
    context['idcname'] = idcname

    # 获取要编辑的设备
    equipment_obj = models.Equipmen.objects.get(id=int(equipment_id))

    if request.method == 'GET':
        cabinet_chuices = models.Cabinet.objects.filter(
            idc__name=idcname).values_list('id', 'number')
        equipment_form = model_forms.EquipmentForms(
            cabinet_chuices, instance=equipment_obj)
        ipaddr_form = IpAddressFormSet(
            queryset=equipment_obj.ipaddress_set.all(), prefix='ip')
        portinfo_form = PortInfoFormSet(
            queryset=equipment_obj.self_equipment.all(), prefix='port')
        context['equipment_form'] = equipment_form
        context['ipaddr_form'] = ipaddr_form
        context['portinfo_form'] = portinfo_form
        return render(request, 'dc_info/create_equipment.html', context)
    if request.method == 'POST':
        cabinet_chuices = models.Cabinet.objects.filter(
            idc__name=idcname).values_list('id', 'number')
        equipment_form = model_forms.EquipmentForms(
            cabinet_chuices, request.POST, instance=equipment_obj)
        ipaddr_form = IpAddressFormSet(
            request.POST,
            queryset=equipment_obj.ipaddress_set.all(),
            prefix='ip')
        portinfo_form = PortInfoFormSet(
            request.POST,
            queryset=equipment_obj.self_equipment.all(),
            prefix='port')
        context['equipment_form'] = equipment_form
        context['ipaddr_form'] = ipaddr_form
        context['portinfo_form'] = portinfo_form
        if equipment_form.is_valid() and ipaddr_form.is_valid() and portinfo_form.is_valid():
            eq_obj = equipment_form.save()
            ip_obj = ipaddr_form.save(commit=False)
            # 循环需要删除的IP地址信息
            for i in ipaddr_form.deleted_objects:
                i.delete()
            for ip in ip_obj:
                ip.equipmen = eq_obj
                ip.save()
            port_obj = portinfo_form.save(commit=False)
            # 循环需要删除的端口信息
            for i in portinfo_form.deleted_objects:
                i.delete()
            for port in port_obj:
                port.self_equipment = eq_obj
                port.save()
            return redirect(
                '/equipmen/%s/%s/?addequipment=%s' %
                (dcname, idcname, equipment_obj))
        else:
            return render(request, 'dc_info/create_equipment.html', context)


# 前端获取数据中心数据统计页面
@login_required
def date_stat(request, dcname, idcname):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    return render(request,
                  'dc_info/abnormal.html',
                  {"dc_obj": dc_obj,
                   'customer_obj': customer_obj,
                   'dcname': dcname,
                   'idcname': idcname})


# 访问客户设备操作日志
@login_required
def customer_equipmen_log(request):
    current_page = request.GET.get('page', 1)
    if request.method == 'POST':
        equipment_sn = request.POST.get('equipment_sn')
        equipment_log_obj = models.EquipmenLog.objects.filter(
            serial_num=equipment_sn).order_by('handle_date').reverse()
    else:
        equipment_log_obj = models.EquipmenLog.objects.all().order_by('handle_date').reverse()

    paginator = CustomPaginator(current_page, 5, equipment_log_obj, 11)
    try:
        data_list = paginator.page(current_page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return render(request,
                  'dc_info/customer_equipmen_log.html',
                  {'page_list': data_list})


# 网络设备端口处理函数
def handel_other_obj(other_obj):
    other_cabiner = '%s' % other_obj.cabinet
    other_mode = '%s %s' % (other_obj.manufacturers, other_obj.model_num)
    other_sn = other_obj.serial_num
    return (other_cabiner, other_mode, other_sn)


# 获取网络设备端口互联
def show_network_port(request):
    data = []
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        equipment_obj = models.Equipmen.objects.get(id=int(equipment_id))
        self_cabinet = '%s' % equipment_obj.cabinet
        self_mode = '%s%s' % (equipment_obj.manufacturers,
                              equipment_obj.model_num)
        self_sn = equipment_obj.serial_num

        for i in equipment_obj.self_equipment.all():
            other_obj = i.up_equipment
            self_port = i.self_equipment_port
            other_cabiner, other_mode, other_sn = handel_other_obj(other_obj)
            other_port = i.up_equipment_port
            data.append([self_cabinet, self_mode, self_sn, self_port,
                         other_cabiner, other_mode, other_sn, other_port])
        for i in equipment_obj.up_equipment.all():
            other_obj = i.self_equipment
            self_port = i.up_equipment_port
            other_cabiner, other_mode, other_sn = handel_other_obj(other_obj)
            other_port = i.self_equipment_port
            data.append([self_cabinet, self_mode, self_sn, self_port,
                         other_cabiner, other_mode, other_sn, other_port])
        return HttpResponse(json.dumps({'status': True, 'data': data}))


# 编辑设备页面Select框获取数据
@login_required
def equipment_getinfo(request, name):
    info_id = request.POST['id']
    data = None
    if name == 'idc':
        data = list(
            models.DcInfo.objects.get(
                id=info_id).idcinfo_set.all().values_list(
                'id', 'name'))
        data.insert(0, ('', '机房'))
    elif name == 'cabinet':
        data = list(
            models.IDCInfo.objects.get(
                id=info_id).cabinet_set.all().values_list(
                'id', 'number'))
        data.insert(0, ('', '机柜'))
    elif name == 'equipment':
        data = list(
            models.Cabinet.objects.get(
                id=info_id).equipmen_set.all().values_list(
                'id',
                'manufacturers',
                'model_num',
                'serial_num'))
        data.insert(0, ('', '厂商', '型号', 'SN'))
    elif name == 'dc':
        data = list(models.DcInfo.objects.all().values_list('id', 'name'))
        data.insert(0, ('', '数据中心'))

    return HttpResponse(json.dumps({'data': data}))
