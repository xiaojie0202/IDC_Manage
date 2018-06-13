from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
from IDC_Manage import settings
from dc_info.model_forms import ChangePasswordForm


# 个人信息页面
def userprofile(request):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    if request.method == 'GET':
        password_form = ChangePasswordForm(request.user.get_username())
        return render(request, 'dc_info/userprofile.html',
                      {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'forms': password_form})
    elif request.method == 'POST':
        password_form = ChangePasswordForm(request.user.get_username(), request.POST)
        if password_form.is_valid():
            password = password_form.cleaned_data.get('password2')
            user = request.user
            user.set_password(password)
            user.save()
            return redirect(settings.LOGIN_URL)
        else:
            return render(request, 'dc_info/userprofile.html',
                          {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'forms': password_form})

