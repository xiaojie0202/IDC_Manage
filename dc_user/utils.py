from django.core.files.storage import FileSystemStorage


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

        # 重写 _save方法

    def _save(self, name, content):
        print(name)
        return super(ImageStorage, self)._save(name, content)