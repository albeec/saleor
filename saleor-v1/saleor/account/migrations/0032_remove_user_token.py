# Generated by Django 2.2.4 on 2019-08-22 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("account", "0031_auto_20190719_0745")]

    operations = [migrations.RemoveField(model_name="user", name="token")]
