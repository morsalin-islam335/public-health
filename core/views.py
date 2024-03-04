from django.shortcuts import render

# Create your views here.

from vaccine.models import Schedule
from vaccine.models import Vaccine, Review

def home(request):
    vaccines = Vaccine.objects.all() 
    reviews = Review.objects.all()
    
    return render(request, "home.html", {'vaccines': vaccines, "reviews": reviews})

    