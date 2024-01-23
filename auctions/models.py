from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=128, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Interaction(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Bid(Interaction):
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} bid {self.bid_amount} on {self.listing.title} "

class Comment(Interaction):
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"