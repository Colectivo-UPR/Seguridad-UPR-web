# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='owner',
        ),
    ]
