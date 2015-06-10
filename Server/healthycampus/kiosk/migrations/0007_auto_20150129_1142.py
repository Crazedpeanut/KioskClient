# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0006_auto_20150129_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='distance_travelled_km',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
