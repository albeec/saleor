# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 01:12
from __future__ import unicode_literals

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("product", "0022_auto_20161212_0301")]

    operations = [
        migrations.AddField(
            model_name="productvariant",
            name="attributes_postgres",
            field=django.contrib.postgres.fields.hstore.HStoreField(
                default={}, verbose_name="attributes"
            ),
        )
    ]
