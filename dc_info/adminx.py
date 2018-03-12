import xadmin
from xadmin import views
from dc_info import models

# Register your models here.


class DcInfoAdmin(object):
    def get_idc_count(self, obj):
        # 获取数据中心所有机房数量
        return obj.idcinfo_set.count()
    get_idc_count.short_description = "机房数量"
    list_display = [
        'name',
        'address',
        'info',
        'material',
        'phon',
        'get_idc_count']
    list_filter = ['name']
    search_fields = ['name', 'phon']
    # fields = (('name', 'address'), 'info') #设置在修改页面排列成1行


class IDCInfoAdmin(object):
    def get_cabinet_count(self, obj):
        # 获取机房的机柜数量
        return obj.cabinet_set.count()
    get_cabinet_count.short_description = '机柜数量'

    list_display = [
        'dc',
        'name',
        'get_cabinet_count',
        'info',
        'principal',
        'principal']
    list_filter = ['dc']
    search_fields = ['name', 'principal']


class CabinetAdmin(object):
    list_display = [
        'get_dc',
        'idc',
        'number',
        'customer',
        'get_equipmen_count',
        'get_occupy',
        'open_date',
    ]
    search_fields = ['number']
    list_editable = ['status']
    list_filter = ['idc', 'customer']
    date_hierarchy = 'open_date'


class CustomerAdmin(object):

    list_display = ['name', 'get_cabinet_count', 'get_equipment_count', 'info']
    search_fields = ['name']


class IpaddreInline(object):
    model = models.IpAddress
    extra = 1


class EquipmenAdmin(object):
    list_display = [
        'get_dc',
        'cabinet',
        'equipment_type',
        'manufacturers',
        'model_num',
        'serial_num',
        'equipment_u',
        'get_ip',
        'get_mask',
        'get_gateway',
        'place_u',
        'up_date',
        'customer']
    list_filter = ['cabinet']
    list_editable = ['equipment_type', 'place_u', 'customer']
    search_fields = ['serial_num', 'get_ip']
    filter_horizontal = ['ipaddress']
    inlines = [IpaddreInline]


class IpAddressAdmin(object):

    list_display = ['ipaddre', 'netmask', 'gateway', 'tags']
    list_editable = ['ipaddre', 'netmask', 'gateway', 'tags']
    search_fields = ['ipaddre']


class PortInfoAdmin(object):
    list_display = [
        'self_equipment',
        'self_equipment_port',
        'up_equipment',
        'up_equipment_port']


class InventoryAdmin(object):
    list_display = [
        'idc',
        'place',
        'name',
        'name_num',
        'sn',
        'count',
        'customer',
        'get_status']


class CabinetLogAdmin(object):
    list_display = [
        'handle_user',
        'handle_type',
        'handle_date',
        'cabinet_dc',
        'cabinet_idc',
        'cabinet_number',
        'customer',
        'dc_surplus_count']


class EquipmenLogAdmin(object):
    list_display = [
        'handle_user',
        'handle_type',
        'handle_date',
        'customer',
        'model_num',
        'serial_num',
        'ipaddre']


class AbnormalInfoAdmin(object):
    list_display = ['equipment', 'info', 'schedule', 'find_time']
    list_filter = ['schedule']
    search_fields = ['equipment']


xadmin.site.register(models.DcInfo, DcInfoAdmin)
xadmin.site.register(models.IDCInfo, IDCInfoAdmin)
# xadmin.site.register(models.Cabinet, CabinetAdmin)
xadmin.site.register(models.Customer, CustomerAdmin)
# xadmin.site.register(models.Equipmen, EquipmenAdmin)
# xadmin.site.register(models.IpAddress, IpAddressAdmin)
# xadmin.site.register(models.PortInfo, PortInfoAdmin)
# xadmin.site.register(models.Inventory, InventoryAdmin)
xadmin.site.register(models.CabinetLog, CabinetLogAdmin)
xadmin.site.register(models.EquipmenLog, EquipmenLogAdmin)
# xadmin.site.register(models.AbnormalInfo, AbnormalInfoAdmin)


class GlobalSetting(object):
    site_title = "IDC资产管理系统"
    site_footer = "2017 by小杰 All rights reserved"


xadmin.site.register(views.CommAdminView, GlobalSetting)
