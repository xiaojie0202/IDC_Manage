from django.db.models.signals import post_save, pre_delete, post_delete



def cabinet_save_log(sender, *args, **kwargs):
    from dc_info.models import Cabinet
    if isinstance(sender(), Cabinet):
        if kwargs['created']:
            print('创建了一个机柜')
            print(kwargs['instance'])


def cabinet_del_log(sender, *args, **kwargs):
    from dc_info.models import Cabinet
    if isinstance(sender(), Cabinet):
        print('删除一个机柜')
        log = kwargs['instance']
        print(log)


post_save.connect(cabinet_save_log)
pre_delete.connect(cabinet_del_log)



