from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('AuctionListing', related_name='watchlist', blank=True)

class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=128, blank=True, null=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name="seller")
    is_active = models.BooleanField(default=True)
    watched_by = models.ManyToManyField('User', related_name="watched", blank=True)
    bids = models.ManyToManyField('Bid', related_name="bids_on_listing", blank=True)
    current_bidder = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.ManyToManyField('Comment', related_name="comments_on_listing", blank=True)


    def __str__(self):
        return self.title

    def get_bid_count(self):
        return self.bids.count()


class Bid(models.Model):
    listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, related_name = "listing_bids")
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} bid {self.bid_amount} on {self.listing.title}"

class Comment(models.Model):
    listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, related_name="listing_comments")
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"
