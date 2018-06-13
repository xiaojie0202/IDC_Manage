# -*- coding:utf-8 -*-
import xadmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from dc_user.models import UserProfile
from xadmin.plugins.auth import PermissionModelMultipleChoiceField
from xadmin.layout import Fieldset, Main, Side
from django.contrib.auth import password_validation


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="密码",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="重新输入密码",
        widget=forms.PasswordInput,
        strip=False,
        help_text="为了校验，请输入与上面相同的密码。",
    )

    class Meta:
        model = UserProfile
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "原始密码不存储，所以没有办法看到这个用户的密码，但可以使用 <a href=\"../password/\">这个表单</a> 来更改密码 。"
        ),
    )

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class UserProfileAdmin(object):
    change_user_password_template = None
    list_display = ('email', 'name', 'birthday', 'create_date')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name', 'birthday')
    ordering = ('email',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(UserProfileAdmin, self).get_field_attrs(db_field, **kwargs)
        if db_field.name == 'user_permissions':
            attrs['form_class'] = PermissionModelMultipleChoiceField
        return attrs

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserProfileAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'email', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(('基本信息'),
                             'name', 'birthday', 'head_img'
                             ),
                    Fieldset(('权限控制'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(('重要信息'),
                             'last_login', 'create_date', 'first_ip'
                             ),
                ),
                Side(
                    Fieldset(('状态'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserProfileAdmin, self).get_form_layout()


xadmin.site.unregister(UserProfile)
#
xadmin.site.register(UserProfile, UserProfileAdmin)
