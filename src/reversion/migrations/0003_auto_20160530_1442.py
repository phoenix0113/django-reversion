# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reversion', '0002_auto_20141216_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='object_id',
            field=models.CharField(help_text='Primary key of the model under version control.', max_length=191),
        ),
        migrations.RemoveField(
            model_name='version',
            name='object_id_int',
        ),
        migrations.AlterIndexTogether(
            name='version',
            index_together=set([('object_id', 'content_type')]),
        ),
    ]