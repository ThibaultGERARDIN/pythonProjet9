from django.shortcuts import render, redirect
from reviews.forms import CreateTicketForm, CreateReviewForm, FollowUserForm
from reviews.models import Ticket, Review, UserFollows
from django.contrib.auth.models import User
from django import forms

# Create your views here.


def feed(request):
    user = request.user
    return render(request, "reviews/feed.html", {"user": user})


def posts(request):
    user = request.user
    if Ticket.objects.all().filter(user=user):
        tickets = Ticket.objects.all().filter(user=user)
    # if Review.objects.get(user=user):
    #     reviews = Review.objects.get(user=user)

    return render(request, "reviews/posts.html", {"user": user, "tickets": tickets})


def subscriptions(request):
    current_user = request.user
    users_list = User.objects.all()
    usernames_list = []
    for user in users_list:
        usernames_list.append(user.username)

    if request.method == "POST":
        form = FollowUserForm(request.POST)
        followed_username = form["user_to_follow"].value()
        if followed_username in usernames_list:
            if form.is_valid():
                UserFollows.objects.create(
                    user=current_user, followed_user=User.objects.get(username=followed_username)
                )
                return redirect("feed")
        else:
            print(f"${followed_username} not in the list")
    else:
        form = FollowUserForm()

    following = UserFollows.objects.all().filter(user=current_user)

    followed_by = UserFollows.objects.all().filter(followed_user=current_user)

    return render(
        request, "reviews/subscriptions.html", {"form": form, "following": following, "followed_by": followed_by}
    )


def ticket_create(request):

    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save(user=request.user)
            return redirect("posts")
    else:
        form = CreateTicketForm()

    return render(request, "reviews/add_ticket.html", {"form": form})


def review_create(request):
    user = request.user
    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST, request.FILES)
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
