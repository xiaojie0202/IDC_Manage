from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def minttags(filter):
    if not filter:
        return ''
    else:
        ele = '&filter=%s' % filter
        return mark_safe(ele)


@register.simple_tag
def equipment_condition(filter, type):
    ele = ''
    if type == 'page' and filter:
        for k, v in filter.items():
            ele += "&%s=%s" % (k, v)
    elif type == 'cabinet_id' and filter.get('customer_id'):
        ele += '&customer_id=%s' % filter.get('customer_id')
    elif type == 'customer_id' and filter.get('cabinet_id'):
        ele += '&cabinet_id=%s' % filter.get('cabinet_id')
    else:
        return ''
    return mark_safe(ele)


# 异常告警页面用于拼接GET请求
@register.simple_tag
def abnormal_condition(filter, type):
    ele = ''
    if filter and type == 'page':
        for k, v in filter.items():
            ele += "&%s=%s" % (k, v)
    elif type == 'schedule' and filter.get("search_abnormal"):
        ele += '&search_abnormal=%s' % filter.get('search_abnormal')
    else:
        return ''
    return ele


# 客户机柜日志页面拼接GET请求
@register.simple_tag
def customet_cabinet_log(filter, type):
    ele = ''
    if filter and type == 'page':
        for k, v in filter.items():
            ele += "&%s=%s" % (k, v)
    elif type == 'cabinet_number' and filter.get('customer'):
        ele += '<input type="hidden" name="customer" value="%s">' % filter.get(
            'customer')
    else:
        return ''

    return mark_safe(ele)


# 编辑机柜解决显示机柜的问题
@register.simple_tag
def hendel_date(date, field):
    if date == 'up_date':
        da = str(field.value())
        da.replace('-', '/')
        field.initial = da
        return field
    else:
        return field
