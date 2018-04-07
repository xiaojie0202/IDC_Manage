from dc_info import models
from django import forms
from django.forms import widgets as ws, fields
from django.forms.models import modelformset_factory


class EquipmentForms(forms.ModelForm):
    class Meta:
        model = models.Equipmen
        fields = '__all__'
        widgets = {
            'up_date': ws.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'}),
        }

    def __init__(self, cabinet_choices=(), *args, **kwargs):
        super(EquipmentForms, self).__init__(*args, **kwargs)
        self.fields['cabinet'].widget.choices = cabinet_choices
        # for field_name in self.base_fields:
        #     field = self.base_fields[field_name]
        #     field.widget.attrs.update({'class': 'form-control'})


class IpAddressForms(forms.ModelForm):
    class Meta:
        model = models.IpAddress
        fields = '__all__'
        exclude = ['equipmen']
        widgets = {
            'tags': ws.TextInput(attrs={'class': 'form-control'}),
            'ipaddre': ws.TextInput(attrs={'class': 'form-control'}),
            'gateway': ws.TextInput(attrs={'class': 'form-control'}),
            'netmask': ws.TextInput(attrs={'class': 'form-control'})
        }


class PortInfoForms(forms.ModelForm):
    dcname = fields.CharField(
        widget=ws.Select(
            attrs={
                'class': 'form-control',
                'onchange': 'getDcChange($(this))'}),
        label='数据中心',
        required=False)
    idcname = fields.CharField(
        widget=ws.Select(
            attrs={
                'class': 'form-control',
                'onchange': 'getIdcChange($(this))'}),
        label='机房',
        required=False)
    cabinet = fields.CharField(
        widget=ws.Select(
            attrs={
                'class': 'form-control',
                'onchange': 'getCabinetChange($(this))'}),
        label='机柜',
        required=False)

    class Meta:
        model = models.PortInfo
        fields = ['self_equipment_port', 'up_equipment', 'up_equipment_port']
        exclude = ['self_equipment']
        widgets = {
            'self_equipment_port': ws.TextInput(
                attrs={
                    'class': 'form-control'}),
            'up_equipment': ws.Select(
                attrs={
                    'class': 'form-control'}),
            'up_equipment_port': ws.TextInput(
                attrs={
                    'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super(PortInfoForms, self).__init__(*args, **kwargs)
        dcname_choices = list(
            models.DcInfo.objects.all().values_list(
                'id', 'name'))
        dcname_choices.insert(0, ('', '数据中心'))
        self.fields['dcname'].widget.choices = dcname_choices
        idcname_choices = list(
            models.IDCInfo.objects.all().values_list(
                'id', 'name'))
        idcname_choices.insert(0, ('', '机房'))
        self.fields['idcname'].widget.choices = idcname_choices
        cabinet_choices = list(
            models.Cabinet.objects.all().values_list(
                'id', 'number'))
        cabinet_choices.insert(0, ('', '机柜'))
        self.fields['cabinet'].widget.choices = cabinet_choices


class InventoryForms(forms.ModelForm):
    class Meta:
        model = models.Inventory
        fields = '__all__'
        widgets = {
            'idc': ws.HiddenInput(),
        }
        labels = {
            'idc': ''
        }

    def __init__(self, *args, **kwargs):
        super(InventoryForms, self).__init__(*args, **kwargs)
        # for field_name in self.base_fields:
        #     field = self.base_fields[field_name]
        #     field.widget.attrs.update({'class': 'form-control'})


# class TestForm(forms.Form):
#     name = fields.CharField(max_length=12, required=True)
#     password = fields.CharField(max_length=12, required=True)
