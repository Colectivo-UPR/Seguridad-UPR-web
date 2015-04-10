# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150408_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaGeografica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormaSeRefirio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MedioNotificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OficialesIntervinieron',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_querella', models.IntegerField()),
                ('nombre', models.CharField(max_length=255)),
                ('turno', models.CharField(max_length=255)),
                ('numero_placa', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perjudicado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_querella', models.IntegerField()),
                ('nombre', models.CharField(max_length=255)),
                ('direccion_residencial', models.CharField(max_length=300)),
                ('direccion_postal', models.CharField(max_length=300)),
                ('telefono', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Querella',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero_caso', models.IntegerField()),
                ('fecha_informada', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'fecha informada')),
                ('medio_notificacion', models.IntegerField()),
                ('hay_fotos', models.BooleanField(default=False)),
                ('official_atendio', models.CharField(max_length=255)),
                ('placa_official', models.CharField(max_length=255)),
                ('referido_a', models.CharField(max_length=255)),
                ('agente_se_notifico', models.CharField(max_length=255)),
                ('placa_agente', models.CharField(max_length=255)),
                ('numero_caso_policia', models.CharField(max_length=255)),
                ('forma_se_refirio', models.IntegerField()),
                ('accion_tomada', models.TextField()),
                ('fecha_incidente', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'fecha incidente')),
                ('lugar_incidente', models.CharField(max_length=255)),
                ('area_incidente', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'A'), (b'B', b'B'), (b'C', b'C')])),
                ('tipo_incidente', models.IntegerField()),
                ('crimen_odio', models.BooleanField(default=False)),
                ('descripcion_incidente', models.TextField()),
                ('sancion_arresto', models.IntegerField()),
                ('area_geografica', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Querellado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_querella', models.IntegerField()),
                ('nombre', models.CharField(max_length=255)),
                ('direccion_residencial', models.CharField(max_length=300)),
                ('direccion_postal', models.CharField(max_length=300)),
                ('telefono', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Querellante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_querella', models.IntegerField()),
                ('nombre', models.CharField(max_length=255)),
                ('direccion_residencial', models.CharField(max_length=300)),
                ('direccion_postal', models.CharField(max_length=300)),
                ('lugar_trabajo', models.CharField(max_length=300)),
                ('tipo_identificacion', models.CharField(max_length=255)),
                ('numero_identificacion', models.CharField(max_length=255)),
                ('tel_trabajo', models.CharField(max_length=30)),
                ('tel_personal', models.CharField(max_length=30)),
                ('sector', models.IntegerField()),
                ('genero', models.CharField(default=b'0', max_length=1, choices=[(b'0', b'F'), (b'1', b'M')])),
                ('email', models.EmailField(max_length=255, verbose_name=b'email address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SancionArresto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sector', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Testigo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_querella', models.IntegerField()),
                ('direccion_residencial', models.CharField(max_length=300)),
                ('direccion_postal', models.CharField(max_length=300)),
                ('telefono', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoIncidente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
