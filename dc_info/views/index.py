from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from dc_info import models
import json
import datetime


# 首页
@login_required
def index(request):
    dc_obj = models.DcInfo.objects.all()
    customer_obj = models.Customer.objects.all()
    dc_obj.idc_count = models.IDCInfo.objects.all().count()
    dc_obj.cabinet_count = models.Cabinet.objects.all().count()
    dc_obj.equipment_count = models.Equipmen.objects.all().count()
    return render(request, 'dc_info/index.html', {"dc_obj": dc_obj, 'customer_obj': customer_obj})


# 机柜增减折线图需要的数据
@login_required
def ajax_cabinet_broken_line(request):
    if request.method == 'POST':
        data = {
            "year": [],
            "dc": [],
            "series": [],
            "options": [],
            "cabinet_count_list": [],
            "customer_name": [],
            "customer_value": [],
            "equipment_value": []
        }
        try:
        # 获取月份
            start_year = models.CabinetLog.objects.all().order_by('date').first().date.year
        except Exception:
            return HttpResponse(json.dumps(data))
        end_year = datetime.datetime.now().date().year
        data["year"] = [str(i) for i in range(start_year, end_year + 1)]
        # 获取数据中心
        name = models.DcInfo.objects.all().values("name")
        data["dc"] = [i["name"] for i in name]
        # series
        for i in data["dc"]:
            data["series"].append({"name": i, "type": "line"})
        # options:
        for index,year in enumerate(data["year"]):
            ser = {"title": {"text": "%s年机柜增减折线图" % year}, "series": []}
            for name in data["dc"]:
                dc_obj = models.DcInfo.objects.get(name=name)
                log_set = dc_obj.cabinetlog_set
                cabinet_count = {"data": []}
                if index == 0:
                    cabinet_count_list = {"value": models.Cabinet.objects.filter(idc__in=dc_obj.idcinfo_set.all()).count(), "name": name}
                    data["cabinet_count_list"].append(cabinet_count_list)
                count = 0
                for month in range(1, 13):
                    a = log_set.filter(date__year=int(year), date__month=month)
                    if a:
                        count = a.order_by("id").last().dc_surplus_count
                        cabinet_count["data"].append(count)
                    else:
                        if month == 1:
                            try:
                                count = log_set.filter(date__year=int(year)-1).order_by('id').last().dc_surplus_count
                            except Exception as e:
                                count = 0
                        cabinet_count["data"].append(count)
                ser["series"].append(cabinet_count)
            data["options"].append(ser)

        # customer_name
        customer_name_dict = models.Customer.objects.all().values("name")
        data["customer_name"] = [i["name"] for i in customer_name_dict]

        # customer_value
        for i in data["customer_name"]:
            customet_obj = models.Customer.objects.get(name=i)
            cabinet_value = customet_obj.cabinet_set.count()
            equipment_count = customet_obj.equipmen_set.count()
            data["customer_value"].append({"value": cabinet_value, "name": i})
            data["equipment_value"].append({"value": equipment_count, "name": i})
        return HttpResponse(json.dumps(data))