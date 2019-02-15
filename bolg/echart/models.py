from django.db import models


class xchart(models.Model):
    data = models.DateField('日期')
    xcount = models.IntegerField('数量')

    def __str__(self):
        return self.data

    class Meta:
        ordering = ['data']
        verbose_name = '统计'
        verbose_name_plural = '统计'
