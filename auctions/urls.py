from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_listing_to_watchlist/<int:listing_id>", views.add_listing_to_watchlist,
         name="add_listing_to_watchlist"),
    path("remove_listing_from_watchlist/<int:listing_id>", views.remove_listing_from_watchlist,
         name="remove_listing_from_watchlist"),
    path("make_bid/<int:listing_id>", views.make_bid, name="make_bid"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("user/created", views.user_created, name="user_created"),
    path("user/bided", views.user_bided, name="user_bided"),
    path("user/won", views.user_won, name="user_won")
]
