# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150415_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querella',
            name='numero_caso',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='querella',
            name='referido_a',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
