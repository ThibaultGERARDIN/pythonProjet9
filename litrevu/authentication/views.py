from django.shortcuts import render, redirect
from authentication.forms import CustomUserCreationForm, CustomAuthenticationForm

# from django.contrib.auth.forms import AuthenticationForm


def landing(request):
    form = CustomAuthenticationForm()
    return render(request, "authentication/landing.html", {"form": form})


def register(request):

    if request.method != "POST":
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing")

    return render(request, "authentication/register.html", {"form": form})
