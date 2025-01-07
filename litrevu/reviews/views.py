from django.shortcuts import render

# Create your views here.


def flux(request):
    return render(request, "reviews/flux.html")


def posts(request):
    return render(request, "reviews/posts.html")


def subscriptions(request):
    return render(request, "reviews/subscriptions.html")
