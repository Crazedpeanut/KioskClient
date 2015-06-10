# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0019_kiosk_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kiosk',
            name='uuid',
        ),
    ]
