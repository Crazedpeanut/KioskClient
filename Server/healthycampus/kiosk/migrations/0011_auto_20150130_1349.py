# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0010_auto_20150130_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kioskdistance',
            old_name='distance',
            new_name='distance_m',
        ),
    ]
