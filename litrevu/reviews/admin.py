from django.contrib import admin
from reviews.models import Review, Ticket, UserFollows

admin.site.register(Review)
admin.site.register(Ticket)
admin.site.register(UserFollows)

# Register your models here.
