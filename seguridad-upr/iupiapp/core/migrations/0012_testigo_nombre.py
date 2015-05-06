# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150415_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='testigo',
            name='nombre',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
