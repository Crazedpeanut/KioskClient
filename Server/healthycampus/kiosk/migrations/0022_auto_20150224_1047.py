# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0021_auto_20150210_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserKiosksToCheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('kiosk', models.ForeignKey(to='kiosk.Kiosk')),
                ('user', models.ForeignKey(null=True, to='kiosk.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='path',
            name='kiosk',
        ),
        migrations.RemoveField(
            model_name='path',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pathnode',
            name='kiosk',
        ),
        migrations.RemoveField(
            model_name='pathnode',
            name='path',
        ),
        migrations.DeleteModel(
            name='Path',
        ),
        migrations.DeleteModel(
            name='PathNode',
        ),
        migrations.AddField(
            model_name='kiosk',
            name='x',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kiosk',
            name='y',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
