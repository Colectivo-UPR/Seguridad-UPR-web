# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='lat',
            field=models.FloatField(default=18.407633, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alert',
            name='lon',
            field=models.FloatField(default=66.044355, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='lat',
            field=models.FloatField(default=18.407633, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='lon',
            field=models.FloatField(default=66.044355, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phone',
            name='lat',
            field=models.FloatField(default=18.407633, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phone',
            name='lon',
            field=models.FloatField(default=66.044355, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='lat',
            field=models.FloatField(default=18.407633, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='report',
            name='lon',
            field=models.FloatField(default=66.044355, blank=True),
            preserve_default=True,
        ),
    ]
