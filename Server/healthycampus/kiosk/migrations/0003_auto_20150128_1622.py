# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0002_auto_20141230_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heartbeat',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('ip', models.CharField(default='', max_length=12)),
                ('date_server', models.DateTimeField(verbose_name='date checked in on server')),
                ('date_kiosk', models.DateTimeField(verbose_name='date checked in on kiosk')),
                ('kiosk', models.ForeignKey(to='kiosk.Kiosk')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kiosk',
            name='ip',
            field=models.CharField(default='', max_length=12),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kiosk',
            name='latitude',
            field=models.CharField(default='', max_length=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kiosk',
            name='longitude',
            field=models.CharField(default='', max_length=10),
            preserve_default=True,
        ),
    ]
