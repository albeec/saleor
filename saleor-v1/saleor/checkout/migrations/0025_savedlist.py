# Generated by Django 2.2.9 on 2020-04-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0024_wishlist_wishlistline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Savedlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(unique=True)),
                ('product_name', models.CharField(max_length=122)),
            ],
        ),
    ]