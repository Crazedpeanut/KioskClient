# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0003_auto_20150128_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('difficulty', models.CharField(max_length=200, default='')),
                ('kiosk', models.ForeignKey(to='kiosk.Kiosk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PathNode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sequence_number', models.IntegerField()),
                ('kiosk', models.ForeignKey(to='kiosk.Kiosk')),
                ('path', models.ForeignKey(to='kiosk.Path')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
