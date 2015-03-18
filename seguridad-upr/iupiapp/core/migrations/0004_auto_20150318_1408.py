# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_officialsphones'),
    ]

    operations = [
        migrations.RenameField(
            model_name='officialsphones',
            old_name='official_id',
            new_name='official',
        ),
    ]
