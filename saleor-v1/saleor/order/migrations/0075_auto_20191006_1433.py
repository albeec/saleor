# Generated by Django 2.2.5 on 2019-10-06 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0074_auto_20190930_0731")]

    operations = [
        migrations.AlterField(
            model_name="orderline",
            name="product_sku",
            field=models.CharField(max_length=255),
        )
    ]
