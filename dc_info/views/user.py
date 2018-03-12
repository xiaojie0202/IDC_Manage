from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
from IDC_Manage import settings


# 个人信息页面
@login_required
def userprofile(request):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    if request.method == 'GET':
        return render(request, 'dc_info/userprofile.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj})
    elif request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = models.User.objects.get(id=request.user.id)
            user.set_password(password2)
            user.save()
            return redirect(settings.LOGIN_URL)
        else:
            return render(request, 'dc_info/userprofile.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj, 'erro': '两次输入密码不一致！'})
