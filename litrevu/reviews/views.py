from django.shortcuts import render, redirect
from reviews.forms import CreateTicketForm, CreateReviewForm, FollowUserForm
from reviews.models import Ticket, Review, UserFollows
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from django.db.models import CharField, Value

# Create your views here.


def get_users_viewable_reviews(user, page):
    user_follows = UserFollows.objects.all().filter(user=user)
    if page == "feed_page":
        try:
            reviews = Review.objects.all().filter(user=user)
            for user_follow in user_follows:
                followed_reviews = Review.objects.all().filter(user=user_follow.followed_user)
                reviews |= followed_reviews
        except ObjectDoesNotExist:
            print("no reviews")
        return reviews
    elif page == "posts_page":
        try:
            reviews = Review.objects.all().filter(user=user)
        except ObjectDoesNotExist:
            print("no reviews")
        return reviews
    else:
        print("Pas de page selectionnée, veuillez réessayer")


def get_users_viewable_tickets(user, page):
    user_follows = UserFollows.objects.all().filter(user=user)
    if page == "feed_page":
        try:
            tickets = Ticket.objects.all().filter(user=user)
            for user_follow in user_follows:
                followed_tickets = Ticket.objects.all().filter(user=user_follow.followed_user)
                tickets |= followed_tickets
        except ObjectDoesNotExist:
            print("no reviews")
        return tickets
    elif page == "posts_page":
        try:
            tickets = Ticket.objects.all().filter(user=user)
        except ObjectDoesNotExist:
            print("no reviews")
        return tickets
    else:
        print("Pas de page selectionnée, veuillez réessayer")


def feed(request):
    user = request.user
    reviews = get_users_viewable_reviews(user, "feed_page")
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(user, "feed_page")
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    return render(request, "reviews/feed.html", {"user": user, "posts": posts})


def my_posts(request):
    user = request.user
    reviews = get_users_viewable_reviews(user, "posts_page")
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(user, "posts_page")
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    return render(request, "reviews/my_posts.html", {"user": user, "posts": posts})


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
            return redirect("my_posts")
    else:
        form = CreateTicketForm()

    return render(request, "reviews/add_ticket.html", {"form": form})


def review_create(request):

    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST, request.FILES)
        review_form = CreateReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.save(user=request.user)
            ticket_id = ticket.id
            review = review_form.save(commit=False)
            review.ticket = Ticket.objects.get(id=ticket_id)
            review.user = request.user
            review.save()

            return redirect("my_posts")

    else:
        ticket_form = CreateTicketForm()
        review_form = CreateReviewForm()

    return render(request, "reviews/add_review.html", {"ticket_form": ticket_form, "review_form": review_form})
