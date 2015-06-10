# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0009_auto_20150130_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='kioskdistance',
            name='distance',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kioskdistance',
            name='kiosk_one',
            field=models.ForeignKey(null=True, related_name='kiosk_one', to='kiosk.Kiosk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kioskdistance',
            name='kiosk_two',
            field=models.ForeignKey(null=True, related_name='kiosk_two', to='kiosk.Kiosk'),
            preserve_default=True,
        ),
    ]
