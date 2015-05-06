# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150501_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='user_id',
            new_name='owner',
        ),
    ]
