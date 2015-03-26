# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150318_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='authuser',
            name='is_webdirector',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authuser',
            name='is_webmanager',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='authuser',
            name='username',
            field=models.CharField(default=b'', max_length=30, verbose_name=b'username', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='authuser',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
