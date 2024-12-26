from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def landing(request):
    form = UserCreationForm()
    return render(request, 'authentication/landing.html', {'form': form})