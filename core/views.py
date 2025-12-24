from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import UserProfile

from properties.models import Property

# Create your views here.
def home(request):
    qs = Property.objects.filter(is_available=True)
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)

            if profile.preferred_city_area:
                qs = qs.filter(city_area__icontains=profile.preferred_city_area)

            if profile.preferred_property_type:
                qs = qs.filter(property_type=profile.preferred_property_type)

            if profile.max_budget:
                qs = qs.filter(rent__lte=profile.max_budget)

        except UserProfile.DoesNotExist:
            pass

    # Fallback ordering for everyone
    qs = qs.order_by("-created_at")      
    return render(request, 'core/home.html', {
        "properties": qs
    })




def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username= username).exists():
            messages.error(request, "Cant signup username already exists")
            return redirect("signup")
        
        User.objects.create_user(
            username=username,
            password=password
        )
        user =  User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        messages.success(request , "Account Created successfully")
        return redirect("login")
    
    return render(request, "core/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")  # homepage
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")
