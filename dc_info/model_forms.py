from dc_info import models
from django import forms
from django.forms import widgets as ws, fields
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from django.contrib.auth import authenticate


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


class ChangePasswordForm(forms.Form):
    old_password = fields.CharField(required=True, widget=ws.PasswordInput, label='旧密码')
    password1 = fields.CharField(max_length=64, min_length=8, required=True, widget=ws.PasswordInput, label='新密码')
    password2 = fields.CharField(max_length=64, min_length=8, required=True, widget=ws.PasswordInput, label='请重新输入新密码')

    def __init__(self, username, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.username = username

    def clean_old_password(self):
        if not authenticate(username=self.username, password=self.cleaned_data.get('old_password')):
            raise ValidationError('旧密码输入错误')
        else:
            return self.cleaned_data.get('old_password')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 != password1:
            raise ValidationError('两次输入密码不一样')
        else:
            return self.cleaned_data.get('password2')
