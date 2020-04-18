# Generated by Django 2.2.1 on 2019-06-18 09:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations

import saleor.core.utils.json_serializer


class Migration(migrations.Migration):

    dependencies = [("product", "0093_auto_20190521_0124")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="meta",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="producttype",
            name="meta",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        ),
    ]
