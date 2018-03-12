from django.conf.urls import url
from dc_info.views import cabinet
from dc_info.views import equipment
from dc_info.views import index
from dc_info.views import inventory
from dc_info.views import user
from dc_info.views import abnormal
from dc_info.views import customer

urlpatterns = [
    url(r'^$', index.index, name='index'),  # 主页
    url(r'^userprofile/$', user.userprofile, name='userprofile'),  # 个人信息主页s

    url(r'^cabinet/(?P<dcname>.+)/(?P<idcname>.+)/create_cabinet/$',
        cabinet.create_cabinet, name='create_cabinet'),  # 添加机柜
    url(r'^cabinet/(?P<dcname>.+)/(?P<idcname>.+)/import_cabinet/$',
        cabinet.import_cabinet, name='import_cabinet'),  # 导入机柜
    url(r'^cabinet/(?P<dcname>.+)/(?P<idcname>.+)/$',
        cabinet.get_cabinet_info, name='get_cabinet'),  # 访问机柜信息
    url(r'^delete_cabinet/$', cabinet.delete_cabinet,
        name='delete_cabinet'),  # 删除机柜

    url(r'^customet_cabinet_log/$', cabinet.customet_cabinet_log,
        name='customer_cabinet_log'),  # 访问客户机柜操作日志视图

    url(r'^equipmen/(?P<dcname>.+)/(?P<idcname>.+)/(?P<equipment_id>\d+)/$',
        equipment.edit_equipment, name='edit_equipment'),  # 编辑设备信息
    url(r'^equipmen/(?P<dcname>.+)/(?P<idcname>.+)/create_equipment/$',
        equipment.create_equipment, name='create_equipment'),  # 增加设备信息
    url(r'^equipmen/(?P<dcname>.+)/(?P<idcname>.+)/import_equipment/$',
        equipment.import_equipment, name='import_equipment'),  # 批量导入设备信息
    url(r'^equipmen/(?P<dcname>.+)/(?P<idcname>.+)/$',
        equipment.get_equipmen_info, name='get_equipmen'),  # 访问设备信息
    url(r'^delete_equipment/$',
        equipment.delete_equipment,
        name='delete_qeuipment'),
    # 删除设备
    url(r'^selectinput/get_(?P<name>.+)/$',
        equipment.equipment_getinfo),  # 编辑设备时候获取信息

    url(r'^show_network_port/$', equipment.show_network_port,
        name='show_network_port'),  # 查看网络设备互联信息

    url(r'^customer_equipmen_log/$', equipment.customer_equipmen_log,
        name='customer_equipmen_log'),  # 访问客户设备操作体日志视图

    url(r'^inventory/(?P<dcname>.+)/(?P<idcname>.+)/edit_inventory/(?P<inventory_id>\d+)/$',
        inventory.edit_inventory, name='edit_inventory'),  # 编辑库存
    url(r'^inventory/(?P<dcname>.+)/(?P<idcname>.+)/import_inventory/$',
        inventory.bulk_import_inventory, name='import_inventory'),  # 批量导入库存
    url(r'^inventory/(?P<dcname>.+)/(?P<idcname>.+)/add_inventory/$',
        inventory.add_inventory, name='add_inventory'),  # 增加库存
    url(r'^inventory/(?P<dcname>.+)/(?P<idcname>.+)/$',
        inventory.get_inventory, name='inventory'),  # 库存管理
    url(r'^delete_inventory/$', inventory.delete_inventory,
        name='delete_inventory'),  # 删除库存信息
    url(r'^update_inventory_count/(?P<operation>\w+)/$',
        inventory.update_inventory_count),  # 增减库存数量

    url(r'^abnormal/(?P<dcname>.+)/(?P<idcname>.+)/$',
        abnormal.get_abnormal, name='get_abnormal'),  # 访问异常信息

    url(r'^customer/(?P<customet_name>.+)/$',
        view=customer.get_customer, name='get_customer'),  # 获取客户信息
    url(r'^ajax_cabinet_broken_line/$',
        index.ajax_cabinet_broken_line),  # 前端主页获取折线图数据


]
