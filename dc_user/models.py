from django.db import models
from django.contrib.auth.models import (
   BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from dc_user.utils import ImageStorage

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email,
            password=password,
            name=name
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    # 账号
    email = models.EmailField(blank=True, unique=True, verbose_name='邮件地址')
    # 基本信息
    head_img = models.ImageField(upload_to='head/', blank=True, null=True, default='head/user.png', storage=ImageStorage(), verbose_name='头像', )
    name = models.CharField(max_length=64, verbose_name='姓名')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now, verbose_name='加入日期')

    # 登录信息
    first_ip = models.GenericIPAddressField(protocol='IPV4', null=True, blank=True, verbose_name='上次登录IP地址')

    # 权限信息
    is_active = models.BooleanField(default=True, verbose_name='有效', help_text='指明用户是否被认为活跃的。以反选代替删除帐号。')
    is_staff = models.BooleanField(default=False, verbose_name='职员状态', help_text='指明用户是否可以登录到这个管理站点。')

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email
