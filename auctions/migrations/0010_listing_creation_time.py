# Generated by Django 4.1.2 on 2022-10-25 01:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_category_listings_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]