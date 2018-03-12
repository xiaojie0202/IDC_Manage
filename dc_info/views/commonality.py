from dc_info import models
from django.core.paginator import Paginator
from django.utils import timezone


# 分页专用
class CustomPaginator(Paginator):

    def __init__(self, current_page, per_pager_num, *args, **kwargs):
        '''
        :param current_page: 当前页
        :param per_pager_num: 总共需要显示几页
        '''
        self.current_page = int(current_page)
        self.per_pager_num = int(per_pager_num)
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def pager_num_range(self):
        '''
        :return: 返回一个列表，页面显示这些页码
        '''
        if self.num_pages < self.per_pager_num:
            return range(1, self.num_pages+1)
        part = int(self.per_pager_num/2)
        if self.current_page <= part:
            return range(1,self.per_pager_num+1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages-self.per_pager_num+1, self.num_pages+1)
        return range(self.current_page-part, self.current_page+part+1)


# 操作机柜的时候调用此函数增减机柜操作日志
def add_cabinet_log(request, handel_type, cabinet_obj):
    if handel_type:
        date = cabinet_obj.open_date
    else:
        date = timezone.now().date()

    models.CabinetLog.objects.create(
        handle_user_id=request.user.id,
        handle_type=handel_type,
        cabinet_dc=cabinet_obj.idc.dc,
        date=date,
        cabinet_idc=cabinet_obj.idc,
        cabinet_number=cabinet_obj.number,
        customer=cabinet_obj.customer,
        dc_surplus_count=models.Cabinet.objects.filter(idc__in=cabinet_obj.idc.dc.idcinfo_set.all()).count()
    )


# 操作设备的时候调用此函数增减设备操作日志
def add_equipment_log(request, handel_type, equipment_obj):
    ipaddr = '127.0.0.1'
    if equipment_obj.ipaddress_set.all():
        ipaddr = equipment_obj.ipaddress_set.all().first().ipaddre
    models.EquipmenLog.objects.create(
        handle_user_id=request.user.id,
        handle_type=handel_type,
        handle_date=timezone.now(),
        customer=equipment_obj.customer,
        cabinet='%s' % equipment_obj.cabinet,
        model_num='%s %s' % (equipment_obj.manufacturers, equipment_obj.model_num),
        serial_num=equipment_obj.serial_num,
        ipaddre=ipaddr,
    )
