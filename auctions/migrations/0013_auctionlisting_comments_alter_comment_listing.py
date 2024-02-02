# Generated by Django 4.2.9 on 2024-02-02 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auctionlisting_current_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments_on_listing', to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.auctionlisting'),
        ),
    ]
