# Generated by Django 4.2.9 on 2024-02-01 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlisting_watched_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='bids',
            field=models.ManyToManyField(related_name='listing_bids', to='auctions.bid'),
        ),
    ]
