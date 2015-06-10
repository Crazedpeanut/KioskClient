# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0014_checkin_user_seconds_since_last_checkin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='user_seconds_since_last_checkin',
            field=models.FloatField(null=True, default=0),
            preserve_default=True,
        ),
    ]
