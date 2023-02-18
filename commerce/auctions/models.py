from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    starting_bid = models.FloatField()
    current_price = models.FloatField()
    image = models.ImageField(upload_to='images', default=None)
    created = models.DateTimeField(auto_now_add=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User,on_delete=models.CASCADE)
    bid = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bid} by {self.bidder}'


class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.comment} by {self.user}'
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, related_name='watchlist')
    

class Winner(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)