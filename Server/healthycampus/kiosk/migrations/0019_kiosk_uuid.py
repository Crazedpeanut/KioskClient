# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0018_auto_20150202_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='uuid',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
    ]
