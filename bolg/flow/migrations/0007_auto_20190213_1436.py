# Generated by Django 2.1.5 on 2019-02-13 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0006_status_pre_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='status_type',
            field=models.IntegerField(blank=True, choices=[(1, '开始'), (2, '结束'), (3, '串行'), (4, '并行'), (5, '或行'), (6, '合并'), (7, '合或'), (8, '分发')], null=True, verbose_name='状态类型'),
        ),
    ]
