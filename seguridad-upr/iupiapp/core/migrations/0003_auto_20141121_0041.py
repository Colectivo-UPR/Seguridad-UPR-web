# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20141109_0520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('message', models.TextField()),
                ('faculty', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('owner', models.ForeignKey(related_name='incidents', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.RenameField(
            model_name='phone',
            old_name='lugar',
            new_name='place',
        ),
        migrations.RenameField(
            model_name='report',
            old_name='date',
            new_name='pub_date',
        ),
    ]
