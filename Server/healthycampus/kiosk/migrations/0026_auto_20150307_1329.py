# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0025_auto_20150307_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='distance',
            field=models.ForeignKey(null=True, to='kiosk.KioskDistance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkin',
            name='kiosk',
            field=models.ForeignKey(null=True, to='kiosk.Kiosk'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkin',
            name='user',
            field=models.ForeignKey(null=True, to='kiosk.User'),
            preserve_default=True,
        ),
    ]
