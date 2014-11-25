# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
                ('incident_date', models.DateTimeField(verbose_name=b'incident date')),
                ('message', models.TextField()),
                ('faculty', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='incident',
            name='incident_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'incident date'),
            preserve_default=True,
        ),
    ]
