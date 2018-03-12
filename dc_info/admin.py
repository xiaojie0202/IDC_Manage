#
# from dc_info import models
# from django.contrib import admin
#
#
# # Register your models here.
#
# @admin.register(models.DcInfo)
# class DcInfoAdmin(admin.ModelAdmin):
#     def get_idc_count(self, obj):
#         # 获取数据中心所有机房数量
#         return obj.idcinfo_set.count()
#     get_idc_count.short_description = "机房数量"
#     list_display = [
#         'name',
#         'address',
#         'info',
#         'material',
#         'phon',
#         'get_idc_count']
#     list_filter = ['name']
#     search_fields = ['name', 'phon']
#     # fields = (('name', 'address'), 'info') #设置在修改页面排列成1行
#
#
# @admin.register(models.IDCInfo)
# class IDCInfoAdmin(admin.ModelAdmin):
#     def get_cabinet_count(self, obj):
#         # 获取机房的机柜数量
#         return obj.cabinet_set.count()
#     get_cabinet_count.short_description = '机柜数量'
#
#     list_display = [
#         'dc',
#         'name',
#         'get_cabinet_count',
#         'info',
#         'principal',
#         'principal']
#     list_filter = ['dc']
#     search_fields = ['name', 'principal']
#
#
# @admin.register(models.Customer)
# class CustomerAdmin(admin.ModelAdmin):
#     def get_cabinet_count(self, obj):
#         # 获取客户的机柜数量
#         return obj.cabinet_set.count()
#     get_cabinet_count.short_description = '机柜数量'
#
#     def get_equipmen_count(self, obj):
#         # 获取客户的设备数量
#         return obj.equipmen_set.count()
#     get_equipmen_count.short_description = '设备数量'
#
#     list_display = ['name', 'get_cabinet_count', 'get_equipmen_count', 'info']
#     search_fields = ['name']
#
#
# @admin.register(models.Equipmen)
# class EquipmenAdmin(admin.ModelAdmin):
#     list_display = [
#         'cabinet',
#         'equipment_type',
#         'manufacturers',
#         'model_num',
#         'serial_num',
#         'equipment_u',
#         'place_u',
#         'up_date',
#         'customer']
#     # list_editable = ['equipment_type', 'place_u',  'customer']
#     search_fields = ['serial_num']
#     # filter_horizontal = ['ipaddress']
#
#
# @admin.register(models.IpAddress)
# class IpAddressAdmin(admin.ModelAdmin):
#
#     list_display = ['id', 'ipaddre', 'netmask', 'gateway', 'tags']
#     list_editable = ['ipaddre', 'netmask', 'gateway', 'tags']
#     search_fields = ['ipaddre']
#
#
# @admin.register(models.Inventory)
# class InventoryAdmin(admin.ModelAdmin):
#
#     list_display = [
#         'idc',
#         'place',
#         'name',
#         'name_num',
#         'sn',
#         'count',
#         'customer',
#         'get_status']
