# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0015_auto_20150202_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='path',
            name='kiosk',
            field=models.ForeignKey(null=True, to='kiosk.Kiosk'),
            preserve_default=True,
        ),
    ]
