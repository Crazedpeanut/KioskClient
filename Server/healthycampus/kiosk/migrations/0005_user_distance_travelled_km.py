# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0004_path_pathnode'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='distance_travelled_km',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
