# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('header', models.CharField(max_length=200, default='Website Name')),
                ('content', models.TextField(default='Website Name')),
                ('footer', models.CharField(max_length=200, default='Copyright 2014')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
