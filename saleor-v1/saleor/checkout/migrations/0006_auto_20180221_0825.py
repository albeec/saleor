# Generated by Django 2.0.2 on 2018-02-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("checkout", "0005_auto_20180108_0814")]

    replaces = [("cart", "0006_auto_20180221_0825")]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[
                    ("open", "Open - currently active"),
                    ("canceled", "Canceled - canceled by user"),
                ],
                default="open",
                max_length=32,
            ),
        )
    ]
