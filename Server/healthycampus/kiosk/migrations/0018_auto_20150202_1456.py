# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0017_auto_20150202_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heartbeat',
            name='ip',
            field=models.CharField(default='', max_length=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kiosk',
            name='ip',
            field=models.CharField(default='', max_length=15),
            preserve_default=True,
        ),
    ]
