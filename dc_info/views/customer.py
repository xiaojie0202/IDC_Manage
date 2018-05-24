from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
import json
import datetime


@login_required
def get_customer(request, customet_name):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    customer = customer_obj.get(name=customet_name)
    if request.method == 'GET':
        close_cabinet = customer.cabinetlog_set.filter(
            handle_type=0).order_by('handle_date').reverse()
        context = {
            "dc_obj": dc_obj,
            'customer_obj': customer_obj,
            'customer': customer,
            'close_cabinet': close_cabinet}
        return render(request, 'dc_info/customerinfo.html', context)
    elif request.method == 'POST':
        data = {'name': [], 'value': []}
        dc_idc = customer.cabinet_set.values(
            'idc__dc__name', 'idc__name').distinct()
        
        for i in dc_idc:
            dc = i.get('idc__dc__name')
            idc = i.get('idc__name')
            name = "%s-%s" % (dc, idc)
            cabinet_count = customer.cabinet_set.filter(
                idc__dc__name=dc, idc__name=idc).count()
            data['name'].append(name)
            data['value'].append({'value': cabinet_count, 'name': name})
            #
            
        return HttpResponse(json.dumps(data))
