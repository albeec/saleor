# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("account", "0008_auto_20161115_1011")]

    replaces = [("userprofile", "0009_auto_20170206_0407")]

    operations = [
        migrations.AlterModelOptions(
            name="address",
            options={"verbose_name": "address", "verbose_name_plural": "addresses"},
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.AlterField(
            model_name="user",
            name="addresses",
            field=models.ManyToManyField(
                blank=True, to="account.Address", verbose_name="addresses"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email"),
        ),
    ]