from django.shortcuts import render, redirect
from reviews.forms import CreateTicketForm, CreateReviewForm, FollowUserForm

# Create your views here.


def flux(request):
    return render(request, "reviews/flux.html")


def posts(request):
    return render(request, "reviews/posts.html")


def subscriptions(request):
    return render(request, "reviews/subscriptions.html")


def ticket_create(request):
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            ticket = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect("ticket", ticket.id)

    else:
        form = CreateTicketForm()

    return render(request, "reviews/flux/add_ticket.html", {"form": form})
