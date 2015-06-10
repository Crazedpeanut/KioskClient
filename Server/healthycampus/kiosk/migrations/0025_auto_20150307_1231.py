# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0024_auto_20150307_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kiosk',
            name='x',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kiosk',
            name='y',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
    ]
