from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import UserProfile
from .models import PasswordResetRequest, Announcement
from django.http import JsonResponse
from properties.models import Property
from properties.models_owners import OwnerProfile
from django.contrib.auth.decorators import login_required
import json


def format_price(price):
    price = float(price)

    if price >= 10000000:
        return f"{price/10000000:.1f} Cr".replace(".0", "")
    elif price >= 100000:
        return f"{price/100000:.1f} L".replace(".0", "")
    else:
        return f"{int(price):,}"
    
# Create your views here.
def home(request):
    print("loading home")
# views.py — home() and dashboard()
    all_properties = Property.objects.filter(is_available=True)\
        .order_by("-created_at")\
        .prefetch_related("media")   # ← add this one line
    rent_properties = all_properties.filter(listing_type='rent') 
    sale_properties = all_properties.filter(listing_type='sale')
    recommended_properties = None
    popup = Announcement.objects.filter(is_active=True).first()
    print(f"Sending {len(all_properties[:6])} properties to template")
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            qs = Property.objects.filter(is_available=True)
            if profile.preferred_city_area:
                qs = qs.filter(city_area__icontains=profile.preferred_city_area)

            if profile.preferred_property_type:
                qs = qs.filter(property_type=profile.preferred_property_type)

            if profile.max_budget:
                qs = qs.filter(price__lte=profile.max_budget)
            
            if qs.exists():
                recommended_properties = qs

        except UserProfile.DoesNotExist:
            pass
    
    for p in sale_properties:
        p.formatted_price = format_price(p.price)
    # Fallback ordering for everyone 
    return render(request, 'core/home.html', {
        "properties":sale_properties[:6],
        "rent_properties": rent_properties[:12],
        "total_properties": all_properties.count(),
        "recommended_properties":recommended_properties,
        'announcement_popup': popup
    })




def signup(request):
    
    if request.user.is_authenticated:
        return redirect("home")
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

@login_required(login_url='login')
def dashboard(request):
    user = request.user

    # ✅ All properties
    properties = Property.objects.filter(is_available=True).order_by("-created_at")

    # ✅ Recommended (same logic as home)
    recommended_properties = None
    user_preferences = None   
    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
            qs = Property.objects.filter(is_available=True)

            if profile.preferred_city_area:
                qs = qs.filter(city_area__icontains=profile.preferred_city_area)

            if profile.preferred_property_type:
                qs = qs.filter(property_type=profile.preferred_property_type)

            if profile.max_budget:
                qs = qs.filter(price__lte=profile.max_budget)

            if qs.exists():
                recommended_properties = qs

        except UserProfile.DoesNotExist:
            user_preferences=None

    # ✅ Owner check
    is_owner = False
    my_properties = []

    if user.is_authenticated:
        is_owner = OwnerProfile.objects.filter(user=user).exists()

        if is_owner:
            my_properties = Property.objects.filter(owner=user)

    context = {
        "properties": properties,
        "recommended_properties": recommended_properties,
        "is_owner": is_owner,
        "my_properties": my_properties,
        "user_preferences": user_preferences,
    }

    return render(request, "core/dashboard.html", context)
def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # homepage
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")

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




def load_more_properties(request):
    print("Loading more properties")
    offset = int(request.GET.get('offset', 6))
    limit  = int(request.GET.get('limit', 6))
    listing_type = request.GET.get('type', 'all')
    bhk = request.GET.get('bhk', None) 

    qs = Property.objects.filter(is_available=True).order_by('-created_at')
    if listing_type != 'all':
        qs = qs.filter(listing_type=listing_type)
    if bhk:                                      # ← ADD
        qs = qs.filter(property_type__iexact=bhk.replace('bhk','BHK').replace('rk','RK'))

    data = []
    props = list(qs[offset:offset + limit].prefetch_related("media"))
    for p in props:
        all_media = list(p.media.all())
        first_image = next((m for m in all_media if m.media_type == 'image'), None)

        # Build full media list so the modal carousel can show all images/videos
        media_list = []
        for m in all_media:
            media_list.append({
                'url': m.file.url,
                'type': m.media_type,   # 'image' or 'video'
            })

        data.append({
            'id':           p.id,
            'title':        p.title,
            'city_area':    p.city_area,
            'price': format_price(p.price),
            'listing_type': p.listing_type,
            'property_type':p.property_type,
            'description':  p.description,
            'image':        first_image.file.url if first_image else '',
            'media':        media_list,   # ← full gallery for the modal

            'carpet_area': p.carpet_area,
            'built_up_area': p.built_up_area,
            'plot_area': p.plot_area,
        })


    return JsonResponse({
        'properties': data,
        'has_more': qs.count() > offset + limit
    })