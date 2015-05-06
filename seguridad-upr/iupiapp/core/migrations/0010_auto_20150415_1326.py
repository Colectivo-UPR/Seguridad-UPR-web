# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_areageografica_formaserefirio_medionotificacion_oficialesintervinieron_perjudicado_querella_querella'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sector',
            old_name='sector',
            new_name='tipo',
        ),
    ]
