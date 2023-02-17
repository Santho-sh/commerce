from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Winner, Watchlist

from .forms import CreateForm

def index(request):
    if User.is_authenticated:
        return render(request, "auctions/index.html", {'listings':Listing.objects.all()})
    
    else:
        return redirect('/login')
    
def listing(request, id):
    product = Listing.objects.get(pk=id)
    return render(request, 'auctions/listing.html', {'listing':product})
    
def categories(request):
    pass
    
    
def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid:
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            staring_bid = form.cleaned_data['staring_bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            
            staring_bid = float(f"{staring_bid:.2f}")
            
            lg = Listing(title=title, description=description, staring_bid=staring_bid, image=image, category=category)
            lg.save()
            
            return redirect('/')
    else:
        form = CreateForm()
    return render(request, 'auctions/create.html', {'form':form})
    
    
def watchlist(request):
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