# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0007_auto_20150129_1142'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='distance_travelled_km',
            new_name='distance_travelled_m',
        ),
    ]
