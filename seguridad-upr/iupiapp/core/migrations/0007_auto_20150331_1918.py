# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150326_1449'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authuser',
            old_name='is_webdirector',
            new_name='is_director',
        ),
        migrations.RenameField(
            model_name='authuser',
            old_name='is_webadmin',
            new_name='is_official',
        ),
        migrations.RenameField(
            model_name='authuser',
            old_name='is_webmanager',
            new_name='is_shift_manager',
        ),
    ]
