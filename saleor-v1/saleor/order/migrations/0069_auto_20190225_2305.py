# Generated by Django 2.1.4 on 2019-02-26 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0068_order_checkout_token")]

    operations = [
        migrations.AlterField(
            model_name="fulfillmentline",
            name="quantity",
            field=models.PositiveIntegerField(),
        )
    ]
