# Generated by Django 2.1.5 on 2019-01-25 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_name', models.CharField(max_length=100, verbose_name='处理方式')),
            ],
            options={
                'verbose_name': '处理方式',
                'verbose_name_plural': '处理方式',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_name', models.CharField(max_length=100, verbose_name='流程')),
                ('flow_status', models.CharField(choices=[('无效', '无效'), ('启用', '启用')], max_length=100, null=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '流程',
                'verbose_name_plural': '流程',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(help_text='流程所处的状态', max_length=100, verbose_name='状态')),
                ('status_type', models.IntegerField(blank=True, choices=[(1, '开始'), (2, '结束'), (3, '串行'), (4, '并行'), (5, '或行'), (6, '合并'), (7, '合或')], null=True, verbose_name='状态类型')),
            ],
            options={
                'verbose_name': '状态',
                'verbose_name_plural': '状态',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(max_length=100, verbose_name='步骤')),
            ],
            options={
                'verbose_name': '步骤',
                'verbose_name_plural': '步骤',
                'ordering': ['flow__id', 'from_status', 'action'],
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(help_text='用户组', max_length=100, verbose_name='用户组')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
                'ordering': ['id'],
            },
        ),
    ]