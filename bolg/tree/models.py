from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Comments(MPTTModel):
    user = models.ForeignKey('user.User', verbose_name='用户', on_delete = models.PROTECT)
    content = models.TextField('评论')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete = models.PROTECT)
    post = models.ForeignKey('main.Article', verbose_name='文章', on_delete = models.PROTECT)
    created_time = models.DateTimeField('评论时间', auto_now_add=True)

    def __str__(self):
        return self.content

    class MPTTMeta:
        order_insertion_by = ['-created_time']

    class Meta:
        ordering = ['-created_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'
