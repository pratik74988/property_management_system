from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserPreferenences

# Create your views here.

@login_required


def preferences (request):
    profile, _ = UserProfile.objects.get_or_create(user = request.user)
    if request.method == "POST":
        form = UserPreferenences(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("home")
    
    else:
        form = UserPreferenences(instance=profile)
    
    return render(request, "accounts/preferences.html", {"form":form})


