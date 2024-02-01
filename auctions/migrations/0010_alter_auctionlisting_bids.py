# Generated by Django 4.2.9 on 2024-02-01 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auctionlisting_bids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids', to='auctions.bid'),
        ),
    ]
