from django.shortcuts import render, redirect
from reviews.forms import CreateTicketForm, CreateReviewForm, FollowUserForm

# Create your views here.


def flux(request):
    user = request.user
    return render(request, "reviews/flux.html", {"user": user})


def posts(request):
    user = request.user
    return render(request, "reviews/posts.html", {"user": user})


def subscriptions(request):
    user = request.user
    return render(request, "reviews/subscriptions.html", {"user": user})


def ticket_create(request):
    user = request.user
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        form.user = user
        if form.is_valid():
            form.save()
            return redirect("posts")

    else:
        form = CreateTicketForm()

    return render(request, "reviews/add_ticket.html", {"form": form})


def review_create(request):
    user = request.user
    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST)
        review_form = CreateReviewForm(request.POST)
        ticket_form.user = user
        review_form.user = user

        if ticket_form.is_valid() and review_form.is_valid():
            ticket_form.save()
            # review_form.ticket to be defined here ?
            review_form.save()
            return redirect("posts")

    else:
        ticket_form = CreateTicketForm()
        review_form = CreateReviewForm()

    return render(request, "reviews/add_review.html", {"ticket_form": ticket_form, "review_form": review_form})
