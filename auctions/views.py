from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User, Listing, Bid, Comment, Category
from .forms import NewListingForm, CommentForm, BidForm, DivErrorList

def index(request):
    return render(request, "auctions/index.html", {
        "index_title": "Active listings",
        "listings": Listing.objects.all()
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


@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "create_listing_form": NewListingForm(),
        })

    if request.method == "POST":
        form = NewListingForm(request.POST, error_class=DivErrorList)

        if form.is_valid():
            title = form.cleaned_data["title"]
            starting_bid = form.cleaned_data["starting_bid"]
            description = form.cleaned_data["description"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]

            listing = Listing(title=title, starting_bid=starting_bid, description=description,
                              img_url=img_url, creator=request.user, category=category)
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "create_listing_form": form
            })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_listing_in_user_watchlist": listing.is_watched_by_user(request.user),
        "number_of_bids": listing.bid_set.all().count(),
        "comment_form": CommentForm(),
        "bid_form": BidForm()
    })


@login_required
def add_listing_to_watchlist(request, listing_id):
    user = User.objects.get(id=request.user.id)
    listing = Listing.objects.get(id=listing_id)

    user.listings_watched.add(listing)

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def remove_listing_from_watchlist(request, listing_id):
    user = User.objects.get(id=request.user.id)
    listing = Listing.objects.get(id=listing_id)

    user.listings_watched.remove(listing)

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def make_bid(request, listing_id):
    user = User.objects.get(id=request.user.id)
    listing = Listing.objects.get(id=listing_id)

    bid_form = BidForm(request.POST, error_class=DivErrorList)

    if not bid_form.is_valid():
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_listing_in_user_watchlist": listing.is_watched_by_user(request.user),
            "number_of_bids": listing.bid_set.all().count(),
            "comment_form": CommentForm(),
            "bid_form": bid_form
        })

    bid_amount = bid_form.cleaned_data["amount"]

    last_biggest_bid = listing.bid_set.all().order_by("-amount").first()

    if (last_biggest_bid and bid_amount < float(last_biggest_bid.amount)
        or bid_amount < listing.starting_bid):
        return render(request, "auctions/listing.html", {
            "message": "Bid is too low",
            "listing": listing,
            "is_listing_in_user_watchlist": listing.is_watched_by_user(request.user),
            "number_of_bids": listing.bid_set.all().count(),
            "comment_form": CommentForm(),
            "bid_form": bid_form,
        })

    Bid.objects.create(user=user, listing=listing, amount=bid_amount, creation_time=timezone.now()).save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if listing.creator == request.user:
        highest_bid = listing.bid_set.all().order_by("-amount").first()
        if highest_bid == None:
            listing.delete()
            return HttpResponseRedirect(reverse("index"))
        listing.winner = highest_bid.user
        listing.is_closed = True
        listing.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    form = CommentForm(request.POST, error_class=DivErrorList)

    if not form.is_valid():
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_listing_in_user_watchlist": listing.is_watched_by_user(request.user),
            "number_of_bids": listing.bid_set.all().count(),
            "comment_form": form,
            "bid_form": BidForm()
        })

    text = form.cleaned_data["text"]
    comment = Comment.objects.create(author=request.user, text=text, listing_id=listing_id)
    comment.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist_listings = user.listings_watched.all()

    return render(request, "auctions/index.html", {
        "index_title": "Watchlist",
        "listings": watchlist_listings
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category_listings = Listing.objects.filter(category=category.id)
    return render(request, "auctions/index.html", {
        "index_title": category.name,
        "listings": category_listings
    })


def user_created(request):
    listings = Listing.objects.filter(creator=request.user)
    return render(request, "auctions/index_all.html", {
        "index_title": "Listings you've created",
        "listings": listings
    })


def user_bided(request):
    listings_ids = Bid.objects.filter(user=request.user).values('listing_id').distinct()
    listings = Listing.objects.filter(id__in=listings_ids)
    return render(request, "auctions/index_all.html", {
        "index_title": "Listings you've bided",
        "listings": listings
    })


def user_won(request):
    listings = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/index_all.html", {
        "index_title": "Listings you've won",
        "listings": listings
    })
