from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.bid, name="close"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

]