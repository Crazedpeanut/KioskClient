# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0011_auto_20150130_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='distance',
            field=models.ForeignKey(to='kiosk.KioskDistance', null=True),
            preserve_default=True,
        ),
    ]
