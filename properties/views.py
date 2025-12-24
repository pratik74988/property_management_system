from django.shortcuts import render
from .models import Property
from django.contrib.auth.decorators import login_required
# Create your views here.
def property_list(request):
    properties = Property.objects.filter(is_available = True)
    return render(request, 'properties/list.html',  {'properties': properties})


def property_home(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'properties/home.html',
                  {'properties':properties})