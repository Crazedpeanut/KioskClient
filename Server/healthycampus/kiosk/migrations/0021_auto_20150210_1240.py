# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0020_remove_kiosk_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='user_points_earned',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
