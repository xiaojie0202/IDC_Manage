from django.utils.html import format_html
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DcInfo(models.Model):
    '''数据中心信息'''
    name = models.CharField(max_length=64, unique=True, verbose_name='数据中心名称')
    address = models.CharField(
        max_length=192,
        blank=True,
        null=True,
        verbose_name='数据中心地址')
    info = models.TextField(verbose_name='数据中心简介', blank=True, null=True)
    material = models.FileField(
        verbose_name='机房相关资料',
        blank=True,
        null=True,
        upload_to="%s/" %
        name)
    phon = models.CharField(max_length=64, verbose_name='机房值班电话')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dcinfo'
        verbose_name = '数据中心'
        verbose_name_plural = '数据中心'


class IDCInfo(models.Model):
    '''机房信息'''
    dc = models.ForeignKey('DcInfo', verbose_name='所属数据中心')
    name = models.CharField(max_length=128, verbose_name='机房名称')
    info = models.TextField(verbose_name='机房简介', blank=True, null=True)
    principal = models.CharField(
        max_length=64,
        verbose_name='机房负责人',
        blank=True,
        null=True,
        editable=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'idcinfo'
        verbose_name = '机房信息'
        verbose_name_plural = '机房信息'
        unique_together = ('dc', 'name')


class Cabinet(models.Model):
    '''机柜信息'''
    idc = models.ForeignKey('IDCInfo', verbose_name='所属机房')
    number = models.CharField(max_length=64, verbose_name='机柜编号')
    customer = models.ForeignKey('Customer', verbose_name='所属客户')
    open_date = models.DateField(
        verbose_name='机柜开通日期',
        blank=True,
        null=True,
        default=timezone.now)

    def get_occupy(self):
        count = 0
        for i in self.equipmen_set.all():
            count += i.equipment_u
        return count

    def get_equipmen_count(self):
        return len(self.equipmen_set.all())

    def get_dc(self):
        return self.idc.dc

    get_dc.short_description = '数据中心'
    get_equipmen_count.short_description = "设备数量"
    get_occupy.short_description = '已占用U数'

    def __str__(self):
        return '%s-%s' % (self.idc, self.number)

    class Meta:
        unique_together = ('idc', 'number')
        db_table = 'cabinet'
        verbose_name_plural = '机柜信息'
        verbose_name = '机柜信息'


class Customer(models.Model):
    '''客户信息'''
    name = models.CharField(max_length=64, verbose_name='客户名称', unique=True)
    info = models.TextField(verbose_name='客户相关信息', blank=True, null=True)

    def get_cabinet_count(self):
        return self.cabinet_set.all().count()

    def get_equipment_count(self):
        return self.equipmen_set.all().count()

    get_cabinet_count.short_description = '机柜数量'
    get_equipment_count.short_description = '设备数量'

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer'
        verbose_name = '客户信息'
        verbose_name_plural = '客户信息'


class Equipmen(models.Model):
    '''设备信息'''
    cabinet = models.ForeignKey('Cabinet', verbose_name='所属机柜')
    equipment_type_choices = ((1, '服务器设备'), (2, '网络设备'))
    equipment_type = models.PositiveSmallIntegerField(
        choices=equipment_type_choices, verbose_name='设备类型')
    manufacturers = models.CharField(max_length=64, verbose_name='设备厂商')
    model_num = models.CharField(max_length=64, verbose_name='设备型号')
    serial_num = models.CharField(max_length=128, verbose_name='设备SN号')
    equipment_u = models.PositiveSmallIntegerField(verbose_name='设备U数')
    place_u = models.PositiveSmallIntegerField(
        verbose_name='所在机柜U数', blank=True, null=True)
    up_date = models.DateField(
        verbose_name='上架日期',
        blank=True,
        null=True,
        default=timezone.now)
    customer = models.ForeignKey('Customer', verbose_name='所属客户')
    node = models.TextField(verbose_name='设备信息描述', blank=True, null=True)

    def get_ip(self):
        # 获取设备IP地址
        if self.ipaddress_set.all():
            return self.ipaddress_set.all().first().ipaddre
        else:
            return '空'

    def get_mask(self):
        # 获取设备掩码
        if self.ipaddress_set.all():
            return self.ipaddress_set.all().first().netmask
        else:
            return '空'

    def get_gateway(self):
        # 获取设备网关
        if self.ipaddress_set.all():
            return self.ipaddress_set.all().first().gateway
        else:
            return '空'

    def get_dc(self):
        # 获取所属数据中心
        return self.cabinet.idc.dc.name

    get_ip.short_description = 'IP'
    get_mask.short_description = '掩码'
    get_gateway.short_description = '网关'
    get_dc.short_description = '数据中心'

    def __str__(self):
        return "%s-%s:%s" % (self.manufacturers,
                             self.model_num, self.serial_num)

    class Meta:
        unique_together = ('cabinet', 'serial_num')
        db_table = 'equipmen'
        verbose_name = '设备信息'
        verbose_name_plural = '设备信息'


class IpAddress(models.Model):
    '''IP地址细信息'''
    equipmen = models.ForeignKey('Equipmen', verbose_name='设备')
    ipaddre = models.GenericIPAddressField(
        protocol='IPV4', verbose_name='IP地址')
    netmask = models.GenericIPAddressField(
        protocol='IPV4', null=True, blank=True, verbose_name='子网掩码')
    gateway = models.GenericIPAddressField(
        protocol='IPV4', null=True, blank=True, verbose_name='网关地址')
    tags = models.CharField(
        max_length=64,
        verbose_name='IP标签',
        blank=True,
        null=True)

    def __str__(self):
        return '%s' % self.ipaddre

    class Meta:
        unique_together = ('equipmen', 'ipaddre')
        db_table = 'ipaddress'
        verbose_name = 'IPV4地址信息'
        verbose_name_plural = 'IPV4地址信息'


class PortInfo(models.Model):
    '''设备端口对应信息'''
    self_equipment = models.ForeignKey(
        'Equipmen',
        verbose_name="本端设备",
        related_name="self_equipment")
    self_equipment_port = models.CharField(max_length=32, verbose_name="本端端口号")
    up_equipment = models.ForeignKey(
        'Equipmen',
        verbose_name="上联设备",
        related_name="up_equipment")
    up_equipment_port = models.CharField(max_length=32, verbose_name="上联端口号")

    def __str__(self):
        return "%s : %s-%s : %s" % (self.self_equipment,
                                    self.self_equipment_port,
                                    self.up_equipment,
                                    self.up_equipment_port)

    class Meta:
        db_table = 'portinfo'
        verbose_name = "设备端口对应信息"
        verbose_name_plural = "设备端口对应信息"


class Inventory(models.Model):
    '''库存信息'''
    idc = models.ForeignKey('IDCInfo', verbose_name='所属机房')
    place = models.CharField(
        max_length=128,
        verbose_name='位置',
        blank=True,
        null=True)
    name = models.CharField(max_length=128, verbose_name='物品名称')
    name_num = models.CharField(max_length=128, verbose_name='物品型号')
    sn = models.CharField(
        max_length=128,
        verbose_name='SN号',
        blank=True,
        null=True)
    count = models.PositiveIntegerField(verbose_name='物品数量')
    customer = models.ForeignKey('Customer', verbose_name='所属客户')
    node = models.TextField(verbose_name='物品描述', blank=True, null=True)
    post_number = models.CharField(
        verbose_name='物流单号',
        blank=True,
        null=True,
        max_length=128)
    status_choices = ((0, '损坏'), (1, '完好'))
    status = models.PositiveSmallIntegerField(
        choices=status_choices, verbose_name='状态', default=1)

    def get_status(self):
        if self.status:
            return format_html('<span style="color: green;">完好</span>')
        else:
            return format_html('<span style="color: red;">损坏</span>')
    get_status.short_description = "状态"

    def __str__(self):
        return "%s-%s" % (self.idc, self.name)

    class Meta:
        db_table = 'inventory'
        verbose_name_plural = '库存信息'
        verbose_name = '库存信息'


class CabinetLog(models.Model):
    '机柜操作日志'
    handle_user = models.ForeignKey(User, verbose_name='操作用户')
    handle_type_choices = ((0, '关闭'), (1, '开通'),)
    handle_type = models.PositiveSmallIntegerField(
        choices=handle_type_choices, verbose_name='操作类型')
    date = models.DateField(verbose_name='日期')  # 机柜开关日期
    handle_date = models.DateTimeField(verbose_name='操作日期', auto_now_add=True)
    cabinet_dc = models.ForeignKey(DcInfo, verbose_name='机柜所属数据中心')
    cabinet_idc = models.ForeignKey('IDCInfo', verbose_name='所属机房')
    cabinet_number = models.CharField(max_length=64, verbose_name='机柜编号')
    customer = models.ForeignKey('Customer', verbose_name='所属客户')
    dc_surplus_count = models.IntegerField(verbose_name='数据中心剩余机柜数量')

    def get_handle_type(self):
        if self.handle_type == 0:
            return format_html('<span style="color: green;">关闭</span>')
        else:
            return format_html('<span style="color: red;">开通</span>')
    get_handle_type.short_description = "状态"

    def __str__(self):
        if self.handle_type == 0:
            return '%s%s%s-%s-%s' % (self.customer,
                                     '关闭',
                                     self.cabinet_dc,
                                     self.cabinet_idc,
                                     self.cabinet_number)
        else:
            return '%s%s%s-%s-%s' % (self.customer,
                                     '开通',
                                     self.cabinet_dc,
                                     self.cabinet_idc,
                                     self.cabinet_number)

    class Meta:
        db_table = 'cabinetlog'
        verbose_name = '机柜日志'
        verbose_name_plural = '机柜日志'


class EquipmenLog(models.Model):
    '''设备操作日志'''
    handle_user = models.ForeignKey(User, verbose_name='操作用户')
    handle_type_choices = ((0, '下架'), (1, '上架'),)
    handle_type = models.PositiveSmallIntegerField(
        choices=handle_type_choices, verbose_name='操作类型')
    handle_date = models.DateTimeField(verbose_name='操作日期')
    customer = models.ForeignKey('Customer', verbose_name='所属客户')
    cabinet = models.CharField(max_length=64, verbose_name='下架机柜')
    model_num = models.CharField(max_length=64, verbose_name='设备型号')
    serial_num = models.CharField(max_length=128, verbose_name='设备SN号')
    ipaddre = models.GenericIPAddressField(
        protocol='IPV4', null=True, blank=True, verbose_name='IP地址')

    def __str__(self):
        if self.handle_type:
            return '%s%s%s:%s-%s' % (self.customer,
                                     '上架',
                                     self.model_num,
                                     self.serial_num,
                                     self.ipaddre)
        else:
            return '%s%s%s:%s-%s' % (self.customer,
                                     '下架',
                                     self.model_num,
                                     self.serial_num,
                                     self.ipaddre)

    class Meta:
        db_table = 'equipmenlog'
        verbose_name_plural = '设备操作日志'
        verbose_name = '设备操作日志'


class AbnormalInfo(models.Model):
    equipment = models.ForeignKey('Equipmen', verbose_name="异常设备")
    info = models.TextField(verbose_name="异常信息")
    schedule_choices = ((0, "未处理"), (1, '已处理'))
    schedule = models.PositiveSmallIntegerField(
        verbose_name="进度", choices=schedule_choices)
    find_time = models.DateTimeField(verbose_name="发现时间", default=timezone.now)
    handel_time = models.DateTimeField(
        verbose_name='处理时间', blank=True, null=True)

    class Meta:
        db_table = "abnormalinfo"
        verbose_name_plural = '异常及告警'
        verbose_name = '异常及告警'
