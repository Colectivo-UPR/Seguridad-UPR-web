# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150331_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='telephone',
            field=models.CharField(default=b'', max_length=20),
            preserve_default=True,
        ),
    ]
