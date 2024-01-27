from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing_details, name="listing_details"),
    path("new_listing/", views.new_listing, name="new_listing"),
    path("my_listings/", views.my_listings, name="my_listings")
]
