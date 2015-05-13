# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialsphones',
            name='phone_number',
            field=models.CharField(default=b'', max_length=30),
            preserve_default=True,
        ),
    ]
