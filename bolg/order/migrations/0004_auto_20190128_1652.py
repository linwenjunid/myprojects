# Generated by Django 2.1.5 on 2019-01-28 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20190128_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinstance',
            name='code',
            field=models.IntegerField(blank=True, null=True, verbose_name='状态'),
        ),
    ]
