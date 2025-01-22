from django.shortcuts import render, redirect
from reviews.forms import CreateTicketForm, CreateReviewForm, FollowUserForm
from reviews.models import Ticket, Review, UserFollows
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from itertools import chain
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.


def get_users_viewable_reviews(user, page):
    """
    Function to get all reviews the current user can see.
    Includes his own, followed users, and reviews of his tickets by non followed users.
    """
    user_follows = UserFollows.objects.all().filter(user=user)
    tickets = Ticket.objects.all().filter(user=user)
    if page == "feed_page":
        try:
            reviews = Review.objects.all().filter(user=user)
            for user_follow in user_follows:
                followed_reviews = Review.objects.all().filter(user=user_follow.followed_user)
                reviews |= followed_reviews
            for ticket in tickets:
                ticket_reviews = Review.objects.all().filter(ticket=ticket)
                if ticket_reviews not in reviews:
                    reviews |= ticket_reviews
        except ObjectDoesNotExist:
            print("Pas de critiques")
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
    """
    Function to get all tickets the current user can see.
    Includes his own and followed users.
    """
    user_follows = UserFollows.objects.all().filter(user=user)
    if page == "feed_page":
        try:
            tickets = Ticket.objects.all().filter(user=user)
            for user_follow in user_follows:
                followed_tickets = Ticket.objects.all().filter(user=user_follow.followed_user)
                tickets |= followed_tickets
        except ObjectDoesNotExist:
            print("Pas de tickets")
        return tickets
    elif page == "posts_page":
        try:
            tickets = Ticket.objects.all().filter(user=user)
        except ObjectDoesNotExist:
            print("Pas de tickets")
        return tickets
    else:
        print("Pas de page selectionnée, veuillez réessayer")


@login_required
def feed(request):
    """
    Feed view, shows all user's viewable posts.
    Buttons to add ticket and review.
    """
    user = request.user
    blocked_reviews = []
    reviews = get_users_viewable_reviews(user, "feed_page")
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(user, "feed_page")
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    for review in reviews:
        if review.ticket in tickets and review.user == user:
            blocked_reviews.append(review.ticket)
            print(review.ticket.title)

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, "reviews/feed.html", {"user": user, "posts": posts, "blocked_reviews": blocked_reviews})


@login_required
def my_posts(request):
    """
    Posts view, show all user's posts.
    """
    user = request.user
    blocked_reviews = []
    reviews = get_users_viewable_reviews(user, "posts_page")
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(user, "posts_page")
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    for review in reviews:
        if review.ticket in tickets and review.user == user:
            blocked_reviews.append(review.ticket)
            print(review.ticket.title)

    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)

    return render(request, "reviews/my_posts.html", {"user": user, "posts": posts, "blocked_reviews": blocked_reviews})


@login_required
def subscriptions(request):
    """
    Subscriptions view.
    User can follow / unfollow and see users following.
    """
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
                try:
                    UserFollows.objects.create(
                        user=current_user, followed_user=User.objects.get(username=followed_username)
                    )
                    messages.success(request, f'Vous êtes maintenant abonné à "{followed_username}" !')
                    return redirect("subscriptions")

                except IntegrityError:
                    messages.error(request, "Vous suivez déjà cet utilisateur.")
                    return redirect("subscriptions")
        else:
            messages.error(request, "Erreur : nom d'utilisateur inconnu.")

    else:
        form = FollowUserForm()

    following = UserFollows.objects.all().filter(user=current_user)

    followed_by = UserFollows.objects.all().filter(followed_user=current_user)

    return render(
        request, "reviews/subscriptions.html", {"form": form, "following": following, "followed_by": followed_by}
    )


@login_required
def ticket_create(request):
    """
    Ticket creation view.
    """
    if request.method == "POST":
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save(user=request.user)
            messages.success(request, f'Merci pour votre ticket sur "{ticket.title}" !')
            return redirect("my_posts")
    else:
        form = CreateTicketForm()

    return render(request, "reviews/add_ticket.html", {"form": form})


@login_required
def ticket_update(request, id):
    """
    Ticket update view.
    Same as ticket create with form pre-filled with instance of ticket.
    """
    ticket = Ticket.objects.get(id=id)
    if request.method == "POST" and ticket.user == request.user:
        form = CreateTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            messages.success(request, f'Le ticket "{ticket.title}" a bien été mis à jour.')
            return redirect("my_posts")
    else:
        form = CreateTicketForm(instance=ticket)

    return render(request, "reviews/add_ticket.html", {"form": form, "origin": "update", "ticket": ticket})


@login_required
def review_create(request):
    """
    Review creation view.

    From scratch including ticket creation.
    """

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
            review.rating = review_form["note"].value()
            review.save()
            messages.success(request, f'Merci pour votre critique de "{ticket.title}" !')
            return redirect("my_posts")

    else:
        ticket_form = CreateTicketForm()
        review_form = CreateReviewForm()

    return render(request, "reviews/add_review.html", {"ticket_form": ticket_form, "review_form": review_form})


@login_required
def review_ticket(request, id):
    """
    Review creation view.

    From existing ticket.
    """
    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        review_form = CreateReviewForm(request.POST)

        if review_form.is_valid():
            try:
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.rating = review_form["note"].value()
                review.save()
                messages.success(request, f'Merci pour votre critique de "{ticket.title}" !')
                return redirect("my_posts")
            except IntegrityError:
                messages.error(request, "Erreur : vous avez déjà publié une critique pour ce ticket.")
                return redirect("feed")
    else:
        review_form = CreateReviewForm()

    return render(request, "reviews/add_review.html", {"ticket": ticket, "review_form": review_form})


@login_required
def review_update(request, id):
    """
    Ticket update view.
    Same as review create with form pre-filled with instance of review.
    Can't update the relevent ticket from there.
    """
    review = Review.objects.get(id=id)
    ticket = review.ticket

    if request.method == "POST" and review.user == request.user:
        review_form = CreateReviewForm(request.POST, instance=review)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.rating = review_form["note"].value()
            review.save()
            messages.success(request, f'Votre critique de "{ticket.title}" a bien été mise à jour.')
            return redirect("my_posts")

    elif review.user != request.user:
        messages.error(request, "Erreur : vous n'avez pas le droit de faire ça !")
        return redirect("feed")

    else:
        review_form = CreateReviewForm(instance=review)

    return render(
        request,
        "reviews/add_review.html",
        {"ticket": ticket, "review": review, "review_form": review_form, "origin": "update"},
    )


@login_required
def unfollow(request, id):
    """
    Function to unfollow user.
    """
    user_to_unfollow = UserFollows.objects.get(id=id)
    if request.method == "POST":

        user_to_unfollow.delete()
        messages.success(request, f'Vous êtes désabonné de "{user_to_unfollow.followed_user}".')
        return redirect("subscriptions")

    return render(request, "reviews/unfollow.html", {"user_to_unfollow": user_to_unfollow})


@login_required
def review_delete(request, id):
    """
    Function to delete a review.
    User needs to be the one who created it.
    """
    review = Review.objects.get(id=id)
    if request.method == "POST" and review.user == request.user:

        review.delete()
        messages.success(request, f'Votre critique de "{review.ticket.title}" a bien été supprimée.')

        return redirect("feed")
    elif review.user != request.user:
        messages.error(request, "Erreur : vous n'avez pas le droit de faire ça !")
        return redirect("feed")

    return render(request, "reviews/review_delete.html", {"review": review})


@login_required
def ticket_delete(request, id):
    """
    Function to delete a ticket.
    User needs to be the one who created it.
    """
    ticket = Ticket.objects.get(id=id)
    if request.method == "POST" and ticket.user == request.user:
        ticket.delete()
        messages.success(request, f'Votre ticket "{ticket.title}" a bien été supprimé.')
        return redirect("feed")
    elif ticket.user != request.user:
        messages.error(request, "Erreur : vous n'avez pas le droit de faire ça !")
        return redirect("feed")

    return render(request, "reviews/review_delete.html", {"ticket": ticket})
