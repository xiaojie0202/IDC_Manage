from django.shortcuts import render, redirect
from django.views import View
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login

# Create your views here.


class Login(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('dcinfo:index'))
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            return render(request, 'login.html', {'erro': "用户名或密码错误"})


def acc_logout(request):
    logout(request)
    return redirect(reverse('login'))


def page_no_found(request):
    return render(request, 'erro.html', {'erro': 404, 'info': '别迷失了方向'})


def page_erro(request):
    return render(request, 'erro.html', {'erro': 500, 'info': '服务器挂掉了'})


def permission_denied(request):
    return render(request, 'erro.html', {'erro': 403, 'info': '服务器不能处理此请求'})
