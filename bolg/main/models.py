from django.db import models
# from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Article(models.Model):
    title = models.CharField('标题',max_length=64)
    content = RichTextUploadingField(verbose_name='内容',config_name='Code')
    user = models.ForeignKey('user.User', verbose_name = '作者', on_delete = models.PROTECT, null=True, blank=True)
    publish_time = models.DateTimeField('发布日期', auto_now_add=True)
    last_update_time = models.DateTimeField('最后一次更新日期', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time']
        verbose_name = '博客'
        verbose_name_plural = '博客'

