# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150415_1514'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='owner',
            new_name='user_id',
        ),
    ]
