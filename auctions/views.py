from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, AuctionListing, Bid, Comment
from .utils import paginate_listings
import datetime
from .forms import NewListing, AddBid, AddComment

# Rendering the index page with active listings
def index(request):
    listings = AuctionListing.objects.filter(is_active=True)
    paginated_listings = paginate_listings(request, listings, per_page=12)

    return render(request, 'auctions/index.html', {'listings': paginated_listings})

# Rendering the page with closed listings
def closed_listings(request):
    listings = AuctionListing.objects.filter(is_active=False)
    paginated_listings = paginate_listings(request, listings, per_page=12)

    return render(request, 'auctions/closed_listings.html', {'listings': paginated_listings})

# Handling user login
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


# Rendering details of a specific listing
def listing_details(request,listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    logged_in_user = request.user if request.user.is_authenticated else None

    # Check if user is logged in and handle watchlist logic
    if logged_in_user:
        user_has_bid = Bid.objects.filter(listing=listing, user=logged_in_user).exists()
        watchlist_input = "Remove to Watchlist" if logged_in_user.watchlist.filter(pk=listing.id).exists() else "Add to Watchlist"
    else:
        user_has_bid = False
        watchlist_input = None  


    comment_form = AddComment()
    now = datetime.datetime.now()

    # Handle form submissions for adding comments and managing watchlist
    if request.method == "POST":
        if "comment_form" in request.POST:
            comment_form = AddComment(request.POST)
            if comment_form.is_valid():
                comment = comment_form.cleaned_data["comment"]
                new_comment = Comment(listing=listing, user=request.user, content=comment, dateTime=now )
                new_comment.save()
                listing.comments.add(new_comment)
                listing.save()
    
        elif "watchlist_form" in request.POST:
            # Handle watchlist form logic
            if logged_in_user.watchlist.filter(pk=listing_id).exists():
                logged_in_user.watchlist.remove(listing)
                messages.error(request, f"{listing.title} removed from your watchlist.", extra_tags='watchlist_error')
                return redirect('listing_details', listing_id=listing_id)
            else:
                logged_in_user.watchlist.add(listing)
                messages.success(request, f"{listing.title} added to your watchlist!", extra_tags='watchlist_success')
                return redirect('listing_details', listing_id=listing_id)


    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "user": logged_in_user,
        "form": AddBid(),
        "watchlist_input": watchlist_input,
        "user_has_bid": user_has_bid,
        "commentForm": AddComment(),
        "comments": listing.comments.all()
    })

# Creating a new listing
@login_required
def new_listing(request):
    now = datetime.datetime.now()
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            new_listing = AuctionListing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data['starting_bid'],
                current_bid=form.cleaned_data['starting_bid'],
                image_url=form.cleaned_data['image_url'],
                category=form.cleaned_data['category'].capitalize(),
                creator=request.user, 
                dateTime=now,
            )

            new_listing.save()

            # Add a success message
            messages.success(request, 'Listing created successfully!')          
        else:
            form = NewListing()


    return render(request, "auctions/new_listing.html", {
        "form": NewListing(),
    })

# Rendering user's own listings
@login_required
def my_listings(request):
    listings = AuctionListing.objects.filter(creator=request.user)
    paginated_listings = paginate_listings(request, listings, per_page=12)
    return render(request, "auctions/my_listings.html", {
        "my_listings": paginated_listings
    })

# Closing a listing
@login_required
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id, creator=request.user)
    listing.is_active = False
    listing.save()
    return redirect('listing_details', listing_id=listing_id)

# Adding a bid to a listing
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
        "commentForm": AddComment(),
    })

# Rendering the user's watchlist
@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    paginated_listings = paginate_listings(request, watchlist, per_page=12)
    return render(request, "auctions/watchlist.html", {
        "watchlist": paginated_listings
    })

# Rendering categories
def categories(request):
    categories = AuctionListing.objects.values_list('category', flat=True).distinct()
    return render(request, 'auctions/categories.html', {'categories': sorted(categories)})

# Rendering listings by category
def listings_by_category(request, category):
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    paginated_listings = paginate_listings(request, listings, per_page=12)
    return render(request, 'auctions/listings_by_category.html', {'listings': paginated_listings, 'category': category})