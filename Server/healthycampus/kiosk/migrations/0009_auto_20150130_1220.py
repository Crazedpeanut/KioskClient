# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0008_auto_20150129_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='KioskDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='path',
            name='user',
            field=models.ForeignKey(to='kiosk.User', null=True),
            preserve_default=True,
        ),
    ]
