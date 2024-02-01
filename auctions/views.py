from django import forms
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Bid, Comment


class NewListing(forms.Form):
    title = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control form-group col-6'})
    )
    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control form-group col-6'})
    )
    starting_bid = forms.DecimalField(
        label="",
        max_digits=6,
        decimal_places=2,
        min_value=0.01,
        max_value=9999.99,
        widget=forms.NumberInput(attrs={'placeholder': 'Starting bid', 'class': 'form-control form-group col-6'})
    )
    image_url = forms.URLField(
        label="",
        widget=forms.URLInput(attrs={'placeholder': 'Image URL', 'class': 'form-control form-group col-6'})
    )
    category = forms.CharField(
        label="",
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder': 'Category', 'class': 'form-control form-group col-6'})
    )

class AddBid(forms.Form):
    new_bid = forms.DecimalField(label="", max_digits=6, decimal_places=2, min_value=0.01, max_value=9999.99, widget=forms.NumberInput(attrs={'placeholder': 'Your bid'}))

def index(request):
    return render(request, "auctions/index.html",{
        "listings": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def listing_details(request,listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    logged_in_user = request.user if request.user.is_authenticated else None

    if logged_in_user:
        user_has_bid = Bid.objects.filter(listing=listing, user=logged_in_user).exists()
        watchlist_input = "Remove to Watchlist" if logged_in_user.watchlist.filter(pk=listing.id).exists() else "Add to Watchlist"
    else:
        user_has_bid = False
        watchlist_input = None  


    if request.method == "POST":
        # Check if the listing is already in the user's watchlist
        if logged_in_user.watchlist.filter(pk=listing_id).exists():
            # If it is, remove it from the watchlist
            logged_in_user.watchlist.remove(listing)
            messages.error(request, f"{listing.title} removed in your watchlist.", extra_tags='watchlist_error')
        else:
            # If it's not, add it to the watchlist
            logged_in_user.watchlist.add(listing)
            messages.success(request, f"{listing.title} added to your watchlist!", extra_tags='watchlist_success')

    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "user": logged_in_user,
        "form": AddBid(),
        "watchlist_input": watchlist_input,
        "user_has_bid": user_has_bid,
    })

@login_required
def new_listing(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data['starting_bid'],
                current_bid=form.cleaned_data['starting_bid'],
                image_url=form.cleaned_data['image_url'],
                category=form.cleaned_data['category'],
                creator=request.user  # Assign the logged-in user as the creator
            )

            new_listing.save()
        else:
            form = NewListing()


    return render(request, "auctions/new_listing.html", {
        "form": NewListing()
    })


@login_required
def my_listings(request):
    return render(request, "auctions/my_listings.html", {
        "my_listings": AuctionListing.objects.filter(creator=request.user)
    })


@login_required
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id, creator=request.user)
    listing.is_active = False
    listing.save()
    return redirect('listing_details', listing_id=listing_id)


@login_required
def add_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    if request.method == "POST":
        form = AddBid(request.POST)
        if form.is_valid():
            new_bid_amount = form.cleaned_data["new_bid"]

        if new_bid_amount > listing.current_bid and new_bid_amount >= listing.starting_bid:
            # Create a new bid
            new_bid = Bid(listing=listing, user=request.user, bid_amount=new_bid_amount)
            new_bid.save()

            
            # Update the current bid on the listing
            listing.current_bid = new_bid_amount
            listing.bids.add(new_bid)
            listing.current_bidder = request.user
            listing.save()

            messages.success(request, 'Bid placed successfully!', extra_tags='add_bid_success')

            return redirect('listing_details', listing_id=listing_id)
        else:
            messages.error(request, 'Bid must be greater than the current bid and starting bid.', extra_tags='add_bid_error')
            return redirect('listing_details', listing_id=listing_id)

    else:
        form = AddBid()

    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "user": request.user,
        "form": AddBid(),
    })

    
@login_required
def watchlist(request):
        # Display the user's watchlist
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })