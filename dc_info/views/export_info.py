from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
import xlwt
from dc_info import models


def export_info(request, dcname, idcname, flag):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="%s.xls"' % flag
        if flag == 'cabinet':
            export_cabinet(dcname, idcname, response)
            return response
        elif flag == 'equipment':
            export_equipment(dcname, idcname, response)
            return response
        elif flag == 'inventory':
            export_inventory(dcname, idcname, response)
            return response


# 生成机柜excel文件
def export_cabinet(dcname, idcname, response):
    cabinet_date = models.Cabinet.objects.filter(
        idc__dc__name=dcname,
        idc__name=idcname).order_by(
        'idc',
        'number').values(
        'idc__dc__name',
        'idc__name',
        'number',
        'customer__name',
        'open_date')
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
    sheet = workbook.add_sheet("sheet1")  # 创建工作页
    row0 = ['数据中心', '机房', '机柜编号', '所属客户', '开通日期']
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    num = 1
    for d in cabinet_date:
        sheet.write(num, 0, d.get('idc__dc__name'))
        sheet.write(num, 1, d.get('idc__name'))
        sheet.write(num, 2, d.get('number'))
        sheet.write(num, 3, d.get('customer__name'))
        sheet.write(num, 4, fmat_date(d.get('open_date')))
        num = num + 1
    workbook.save(response)


# 格式化日期
def fmat_date(f_time, format='%Y-%m-%d'):
    """格式化时间"""
    try:
        return f_time.strftime(format)
    except Exception:
        return ''


# 生成设备excel文件
def export_equipment(dcname, idcname, response):
    idc = models.IDCInfo.objects.get(dc__name=dcname, name=idcname)
    cabinet_set = idc.cabinet_set.all()
    equipment_date = models.Equipmen.objects.filter(
        cabinet__in=cabinet_set).order_by(
        'cabinet__idc__dc',
        'cabinet__idc',
        'cabinet__number').values(
        'cabinet__number',
        'equipment_type',
        'manufacturers',
        'model_num',
        'serial_num',
        'equipment_u',
        'place_u',
        'customer__name',
        'up_date')

    workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
    sheet = workbook.add_sheet("sheet1")  # 创建工作页
    row0 = ['数据中心', '机房', '机柜编号', '设备类型', '厂商', '型号', 'SN', 'U数', '机柜位置', '所属客户', '上架日期']
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    num = 1
    for d in equipment_date:
        sheet.write(num, 0, dcname)
        sheet.write(num, 1, idcname)
        sheet.write(num, 2, d.get('cabinet__number'))
        if d.get('equipment_type') == 1:
            sheet.write(num, 3, '服务器设备')
        elif d.get('equipment_type') == 2:
            sheet.write(num, 3, '网络设备')
        else:
            sheet.write(num, 3, None)
        sheet.write(num, 4, d.get('manufacturers'))
        sheet.write(num, 5, d.get('model_num'))
        sheet.write(num, 6, d.get('serial_num'))
        sheet.write(num, 7, d.get('equipment_u'))
        sheet.write(num, 8, d.get('place_u'))
        sheet.write(num, 9, d.get('customer__name'))
        sheet.write(num, 10, fmat_date(d.get('up_date')))
        # sheet.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')
        num = num + 1
    workbook.save(response)


# 生成库存excel文件筐
def export_inventory(dcname, idcname, response):
    idc = models.IDCInfo.objects.get(dc__name=dcname, name=idcname)
    inventory_obj = idc.inventory_set.all()
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
    sheet = workbook.add_sheet("sheet1")  # 创建工作页
    row0 = ['数据中心', '机房', '位置', '名称', '型号', '资产编号', '数量', '所属客户', '描述', '物流单号']
    for i in enumerate(row0):
        sheet.write(0, i[0], i[1])
    num = 1
    for inventory in inventory_obj:
        sheet.write(num, 0, dcname)
        sheet.write(num, 1, idcname)
        sheet.write(num, 2, inventory.place)
        sheet.write(num, 3, inventory.name)
        sheet.write(num, 4, inventory.name_num)
        sheet.write(num, 5, inventory.sn)
        sheet.write(num, 6, inventory.count)
        sheet.write(num, 7, inventory.customer.name)
        sheet.write(num, 8, inventory.node)
        sheet.write(num, 9, inventory.post_number)
        num += 1
    workbook.save(response)
