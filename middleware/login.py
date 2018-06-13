from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


class IsLoginMiddleware(MiddlewareMixin):

    '''用户访问验证中间件'''

    def process_request(self, request):
        if request.path_info != '/login/':
            if not request.user.is_authenticated():
                return redirect(reverse('login'))
            else:
                # 记录用户登陆的IP
                user_ip = request.META['REMOTE_ADDR']
                request.user.first_ip = user_ip
                request.user.save()
