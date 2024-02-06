from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing_details, name="listing_details"),
    path("new_listing/", views.new_listing, name="new_listing"),
    path("my_listings/", views.my_listings, name="my_listings"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path('category/<str:category>/',views.listings_by_category, name='listings_by_category'),

]
