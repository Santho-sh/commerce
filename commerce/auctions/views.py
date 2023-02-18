from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max

from .models import User, Listing, Bid, Comment, Winner, Watchlist

from .forms import CreateForm

def index(request):
    if User.is_authenticated:
        bids = Bid.objects.all()
        highest_bid = bids.aggregate(Max('bid'))['bid__max']
        return render(request, "auctions/index.html", {'listings':Listing.objects.all(),
          'current_price':highest_bid                  
          })

    else:
        return redirect('/login')
    
def listing(request, id):
    
    product = Listing.objects.get(pk=id)
    try:
        bids = Bid.objects.filter(listing=product)
        highest_bid = bids.aggregate(Max('bid'))['bid__max']
        no_bids = bids.count()  
        highest_bidder = Bid.objects.get(listing=product, bid=highest_bid).bidder
        
    
    except Bid.DoesNotExist:
        highest_bid = product.starting_bid
        bids = 0
        highest_bidder = None
    
    comments = Comment.objects.filter(listing=product)
    
    return render(request, 'auctions/listing.html', {
    'listing':product,
    'highest_bid':highest_bid,
    'bids':no_bids,
    'bidder':highest_bidder,
    'comments':comments,
    })

def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            starting_bid = form.cleaned_data.get('starting_bid')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')
            
            starting_bid = float(f"{starting_bid:.2f}")
            user_id = request.user
            
            lg = Listing.objects.create(
                seller=user_id,
                title=title, description=description, starting_bid=starting_bid,
                current_price=starting_bid,
                image=image,
                category=category,
                )
            lg.save()
            
            return redirect('/')
        
    else:
        form = CreateForm()
    return render(request, 'auctions/create.html', {'form':form})
    
    
def bid(request, id):
    if request.method == 'POST':
        bid_amount = float(request.POST['bid'])

        listing = Listing.objects.get(pk=id)
        
        if bid_amount > listing.starting_bid:
            
            bid = Bid.objects.create(
                listing=listing,
                bidder=request.user,
                bid=bid_amount,
                )
            bid.save()
            
            listing = Listing.objects.get(pk=id)
            listing.current_price = bid_amount
            listing.save()
        
    return redirect('/listing/%i' %id)
    
    
def watchlist(request):
    if request.method == 'POST':
        
        id = int(request.POST['id'])
        try:
            watchlist = Watchlist.objects.get(user=request.user)
        except Watchlist.DoesNotExist:
            watchlist = Watchlist.objects.create(user=request.user)
            
        listing = Listing.objects.get(pk=id)
        watchlist.listings.add(listing)
        
        return redirect('/listing/%i' %id)
    
    else:
        try:
            user = Watchlist.objects.get(user=request.user)
            listings_all = user.listings.all()
            
        except Watchlist.DoesNotExist:
            listings_all = None
        
        return render(request, 'auctions/watchlist.html', {'listings':listings_all})


def remove(request):
    if request.method == 'POST':
        id = int(request.POST['id'])
        
        watchlist = Watchlist.objects.get(user=request.user)
        listing = Listing.objects.get(pk=id)
        watchlist.listings.remove(listing)
        
    return redirect('/watchlist')


def comment(request):
    if request.method == 'POST':
        id = int(request.POST['id'])
        comment = request.POST['comment']

        listing = Listing.objects.get(pk=id)
        cmt = Comment.objects.create(comment=comment,
                                     listing=listing,
                                     user=request.user,
                                     )
        cmt.save()
        return redirect('/listing/%i' %id)
    else:
        return redirect('/')


def close(request):
    ...

def categories(request):
    pass


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