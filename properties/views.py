from django.shortcuts import render, redirect
from .models import Property
from django.contrib.auth.decorators import login_required
from .forms import OwnerSignupForm, PropertyRequestForm
from .models_owners import PropertyRequest, Partner, PropertyRequestMedia

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def property_list(request):
    properties = Property.objects.filter(is_available = True)
    return render(request, 'properties/list.html',  {'properties': properties})


def property_home(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'properties/home.html',
                  {'properties':properties})

def owner_signup(request):
    """
    Any visitor can register as a property owner here.
    No admin access is granted — only an OwnerProfile is created.
    """
    if request.user.is_authenticated:
        return redirect("properties:submit_property")
 
    if request.method == "POST":
        form = OwnerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! You can now submit a property listing.")
            return redirect("properties:submit_property")
    else:
        form = OwnerSignupForm()
 
    return render(request, "owner_signup.html", {"form": form})
 
 
# ─────────────────────────────────────────────
#  Submit a property (owner only, login required)
# ─────────────────────────────────────────────
@login_required(login_url="properties:owner_signup")
def submit_property(request):
    """
    Logged-in owners submit a listing request.
    It goes into PropertyRequest with status='pending'
    and is only published after admin approval.
    """
 
    # Show owner's past requests
    my_requests = PropertyRequest.objects.filter(owner=request.user)
 
    if request.method == "POST":
        form = PropertyRequestForm(request.POST, request.FILES)
        if form.is_valid():
            req = form.save(commit=False)
            req.owner = request.user
            req.save()

            # 🔥 HANDLE IMAGES
            images = request.FILES.getlist('images')

            if not images:
                messages.error(request, "Please Upload at least one image.")
                return redirect("properties:submit_property")
            for img in images:
                PropertyRequestMedia.objects.create(
                    property_request=req,
                    file=img,
                    media_type="image"
                )
            messages.success(
                request,
                "Your listing has been submitted for review. "
                "We'll publish it once our team approves it."
            )       
            return redirect("properties:submit_property")
    else:
        form = PropertyRequestForm()
 
    return render(request, "submit_property.html", {
        "form": form,
        "my_requests": my_requests,
    })
 
 
# ─────────────────────────────────────────────
#  Partners page  (public)
# ─────────────────────────────────────────────
def partners(request):
    partner_list = Partner.objects.filter(is_active=True)
    return render(request, "partners.html", {"partners": partner_list})