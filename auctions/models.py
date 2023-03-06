from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    listings_watched = models.ManyToManyField("Listing", blank=True, related_name="watching_users")


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_listing', blank=False)
    img_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=False)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_listing")
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won_listing", blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def get_biggest_bid(self):
        return self.bid_set.all().order_by("-amount").first()

    def is_watched_by_user(self, user):
        if self.watching_users.filter(pk=user.id):
            return True
        return False

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_maker")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_time = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} made bid of {self.amount} to {self.listing}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    text = models.CharField(max_length=400, blank=False)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented {self.listing}"
