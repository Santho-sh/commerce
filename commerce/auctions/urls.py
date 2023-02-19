from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("myListings", views.myListings, name="myListings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("remove", views.remove, name="remove"),
    path("comment", views.comment, name="comment"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

]