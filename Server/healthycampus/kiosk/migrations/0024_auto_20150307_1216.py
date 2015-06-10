# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0023_auto_20150224_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='date',
            field=models.DateTimeField(verbose_name='date checked in', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkin',
            name='distance',
            field=models.ForeignKey(to='kiosk.KioskDistance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkin',
            name='user',
            field=models.ForeignKey(to='kiosk.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkin',
            name='user_seconds_since_last_checkin',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='heartbeat',
            name='date_kiosk',
            field=models.DateTimeField(verbose_name='date checked in on kiosk', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='heartbeat',
            name='date_server',
            field=models.DateTimeField(verbose_name='date checked in on server', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kiosk',
            name='address',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kioskdistance',
            name='distance_m',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kioskdistance',
            name='kiosk_one',
            field=models.ForeignKey(to='kiosk.Kiosk', related_name='kiosk_one'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kioskdistance',
            name='kiosk_two',
            field=models.ForeignKey(to='kiosk.Kiosk', related_name='kiosk_two'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='barcode',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
    ]
