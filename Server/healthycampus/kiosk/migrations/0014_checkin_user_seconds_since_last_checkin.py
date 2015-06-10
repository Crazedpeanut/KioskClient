# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0013_auto_20150202_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='user_seconds_since_last_checkin',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
