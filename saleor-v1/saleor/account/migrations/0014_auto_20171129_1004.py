# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-29 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("account", "0013_auto_20171120_0521")]

    replaces = [("userprofile", "0014_auto_20171129_1004")]

    operations = [
        migrations.AlterModelOptions(name="address", options={}),
        migrations.AlterModelOptions(
            name="user",
            options={
                "permissions": (
                    ("view_user", "Can view users"),
                    ("edit_user", "Can edit users"),
                    ("view_group", "Can view groups"),
                    ("edit_group", "Can edit groups"),
                    ("view_staff", "Can view staff"),
                    ("edit_staff", "Can edit staff"),
                    ("impersonate_user", "Can impersonate users"),
                )
            },
        ),
    ]
