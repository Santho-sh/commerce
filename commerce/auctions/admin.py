from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist, Winner

# Register your models here.

class imageAdmin(admin.ModelAdmin):
    list_display = ["title", "photo"]

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Winner)
