# Generated by Django 2.1.5 on 2019-01-25 02:26

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name='发布日期')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='最后一次更新日期')),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
                'ordering': ['-publish_time'],
            },
        ),
    ]
