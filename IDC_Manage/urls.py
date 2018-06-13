"""IDC_Manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from xadmin.plugins import xversion
from django.views.generic.base import RedirectView
from IDC_Manage import views
from django.conf.urls.static import static
from django.conf import settings
import xadmin
import dc_info.urls


xadmin.autodiscover()
xversion.register_models()


urlpatterns = [
    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout', views.acc_logout, name='logout'),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^', include(dc_info.urls, namespace='dcinfo'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = views.permission_denied
handler404 = views.page_no_found
handler500 = views.page_erro
