from django.contrib import admin
from reviews.models import Review, Ticket, UserFollows

admin.site.register(Review, Ticket, UserFollows)
# Register your models here.
