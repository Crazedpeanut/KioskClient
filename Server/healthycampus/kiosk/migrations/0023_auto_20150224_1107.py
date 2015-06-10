# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0022_auto_20150224_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkioskstocheckin',
            name='user',
            field=models.ForeignKey(to='kiosk.User'),
            preserve_default=True,
        ),
    ]
