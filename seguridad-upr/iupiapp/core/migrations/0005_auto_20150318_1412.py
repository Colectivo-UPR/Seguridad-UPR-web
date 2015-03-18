# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150318_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialsphones',
            name='official',
            field=models.ForeignKey(related_name='phone', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
