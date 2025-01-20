from django.shortcuts import render, redirect
from authentication.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    if request.method != "POST":
        form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Vous êtes bien connecté en tant que \"{user.username}\"")
            return redirect("feed")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
            return redirect("home")
        
    return render(request, "authentication/home.html", {"form": form})


def register(request):

    if request.method != "POST":
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "authentication/register.html", {"form": form})


def logout_view(request):
    user = request.user
    if user is not None:
        logout(request)
        return redirect("home")


def login_view(request):
    if request.method != "POST":
        form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("feed")
        else:
            return print("Erreur dans l'identifiant ou le mdp")
    return render(request, "authentication/login.html", {"form": form})
