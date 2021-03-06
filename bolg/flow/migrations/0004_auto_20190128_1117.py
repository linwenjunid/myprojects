# Generated by Django 2.1.5 on 2019-01-28 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0003_auto_20190125_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='pre_user_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pre_status_user_type', to='flow.UserType', verbose_name='撤回组'),
        ),
        migrations.AlterField(
            model_name='status',
            name='user_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status_user_type', to='flow.UserType', verbose_name='用户组'),
        ),
    ]
