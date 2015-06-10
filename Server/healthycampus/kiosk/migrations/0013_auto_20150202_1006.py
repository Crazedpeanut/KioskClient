# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0012_checkin_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='distance',
            field=models.ForeignKey(default=0, to='kiosk.KioskDistance'),
            preserve_default=True,
        ),
    ]
