# Generated by Django 2.1.5 on 2019-01-25 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0002_auto_20190125_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='from_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_Step', to='flow.Status', verbose_name='开始状态'),
        ),
        migrations.AlterField(
            model_name='step',
            name='to_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_Step', to='flow.Status', verbose_name='结束状态'),
        ),
    ]
