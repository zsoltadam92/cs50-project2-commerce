# Generated by Django 4.2.9 on 2024-02-01 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_auctionlisting_bids_alter_bid_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='current_bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
