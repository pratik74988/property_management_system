from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import UserProfile
from .models import PasswordResetRequest
from django.http import JsonResponse
from properties.models import Property

# Create your views here.
def home(request):
    all_properties = Property.objects.filter(is_available=True).order_by("-created_at")
    recommended_properties = None


    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            qs = Property.objects.filter(is_available=True)
            if profile.preferred_city_area:
                qs = qs.filter(city_area__icontains=profile.preferred_city_area)

            if profile.preferred_property_type:
                qs = qs.filter(property_type=profile.preferred_property_type)

            if profile.max_budget:
                qs = qs.filter(rent__lte=profile.max_budget)
            
            if qs.exists():
                recommended_properties = qs

        except UserProfile.DoesNotExist:
            pass

    # Fallback ordering for everyone 
    return render(request, 'core/home.html', {
        "properties":all_properties,
        "recommended_properties":recommended_properties
    })




def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username= username).exists():
            messages.error(request, "Cant signup username already exists")
            return redirect("signup")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")
        
        user = User.objects.create_user(
                username=username,
                password=password,
                email=email,

            )
       
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

def request_password_reset(request):
    if request.method == "POST":
        username = request.POST.get("username")

        try:
            user = User.objects.get(username =username)
            if PasswordResetRequest.objects.filter(user=user, is_resolved=False).exists():
                return JsonResponse({
                    "status": "error",
                    "msg": "Reset already requested"
                })
            PasswordResetRequest.objects.create(user=user)
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({
                "status":"error",
                "msg":"user not found"
            })
    return JsonResponse({"status":"invalid"})

