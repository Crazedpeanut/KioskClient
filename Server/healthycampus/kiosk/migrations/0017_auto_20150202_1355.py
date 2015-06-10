# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0016_auto_20150202_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='distance',
            field=models.ForeignKey(to='kiosk.KioskDistance', null=True, default=0),
            preserve_default=True,
        ),
    ]
