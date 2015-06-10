# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0005_user_distance_travelled_km'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='distance_travelled_km',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
