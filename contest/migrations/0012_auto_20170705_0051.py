# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-05 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0011_auto_20170705_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='solved_by_whom',
            field=models.ManyToManyField(to='userprof.UserProfile'),
        ),
    ]