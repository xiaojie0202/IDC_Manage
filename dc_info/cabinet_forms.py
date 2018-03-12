from django import forms
from django.forms import widgets
from django.forms import fields
from dc_info import models


class CreateCabinetForms(forms.Form):
    # idc = models.ForeignKey('IDCInfo', verbose_name='所属机房')
    # number = models.CharField(max_length=64, verbose_name='机柜编号')
    # customer = models.ForeignKey('Customer', verbose_name='所属客户')
    # open_date = models.DateField(verbose_name='机柜开通日期', blank=True, null=True, default=datetime.datetime.now().date())
    idc = fields.CharField(required=True)
    number = fields.CharField(required=True,
                              label='<label for="id_number" class="col-sm-2 control-label">机柜编号</label>',
                              widget=forms.TextInput(attrs={'placeholder': "机柜编号", 'class': 'form-control'}))
    customer = fields.CharField(
        required=True,
        widget=forms.Select(attrs={'class': "form-control"}),
        label='<label for="id_customer" class="col-sm-2 control-label">客户</label>'
    )
    open_date = fields.DateField(required=True,
                                 widget=widgets.DateInput)

    def __init__(self, *args, **kwargs):
        super(CreateCabinetForms, self).__init__(*args, **kwargs)
        # self.customer.widget = models.Customer.objects.values_list('id', 'name')
        self.fields['customer'].widget.choices = models.Customer.objects.values_list('id', 'name')