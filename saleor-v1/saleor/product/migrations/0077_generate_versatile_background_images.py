# Generated by Django 2.1.2 on 2018-11-11 16:08
from django.db import migrations


class Migration(migrations.Migration):
    # there was 'thumbnail generation' which already exists ad management command
    # because this migration is depended on, it cannot be removed
    dependencies = [("product", "0076_auto_20181012_1146")]

    operations = []
