# Generated by Django 2.1.5 on 2019-01-28 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderinstance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinstance',
            name='code',
            field=models.IntegerField(null=True, verbose_name='状态'),
        ),
    ]
