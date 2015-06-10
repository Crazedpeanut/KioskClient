# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0026_auto_20150307_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkioskstocheckin',
            name='kiosk',
            field=models.ForeignKey(to='kiosk.Kiosk', null=True),
            preserve_default=True,
        ),
    ]
