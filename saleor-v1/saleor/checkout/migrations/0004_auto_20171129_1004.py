# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-29 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("checkout", "0003_auto_20170906_0556")]

    replaces = [("cart", "0004_auto_20171129_1004")]

    operations = [
        migrations.AlterModelOptions(
            name="cart", options={"ordering": ("-last_status_change",)}
        ),
        migrations.AlterModelOptions(name="cartline", options={}),
    ]
