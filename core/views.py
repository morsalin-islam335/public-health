from django.shortcuts import render

# Create your views here.

from vaccine.models import Schedule
from vaccine.models import Vaccine, Review
from account.models import Account

def home(request):
    vaccines = Vaccine.objects.all() 
    reviews = Review.objects.all()
    doctors = Account.objects.filter(is_doctor = True)
    
    return render(request, "home.html", {'vaccines': vaccines, "reviews": reviews, 'allDoctors': doctors})
    

    

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')
    

def contact(request):
    return render(request, "contact.html")
    