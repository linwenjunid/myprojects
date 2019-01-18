from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.conf import settings


class User(AbstractUser):
    phone_number = models.CharField('手机号码',max_length=11)
    photo = models.ImageField('照片',upload_to="icons/%Y/%m/%d", blank=True, null=True)

    def name(self):
        return self.last_name+self.first_name
    name.short_description = '姓名'

    def show_photo(self):
        return format_html(
            '<img src="{}{}" width="60px"/>'.format(settings.MEDIA_URL,self.photo)
        )

    show_photo.short_description = '图片'

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
