from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from . forms import addVaccineForm, AddScheduleForm, ReviewForm
from django.contrib import messages
# Create your views here.
from . models import Schedule
from django.views.generic import CreateView
from django.urls import reverse_lazy
from . forms import BookDoseForm
from . models import Vaccine_Recipient, Review
from vaccine.models import Vaccine
from datetime import timedelta


from django.shortcuts import HttpResponseRedirect

def addVaccine(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.account.is_doctor:
        messages.error(request, "As a patient, you can not add vaccine")
    
    if request.method  == "POST":
        form = addVaccineForm(request.POST, request.FILES)
        if form.is_valid():
            vaccine = form.save(commit = False)
            vaccine.dose = form.cleaned_data.get("total_dose")
            vaccine.doctor = request.user.account
            vaccine.save()
            messages.success(request, "Add vaccine successfully!")
            return redirect("homepage")
        else:
            messages.error(request, "Your form information is incorrect")

    else:

        form = addVaccineForm()
    return render(request, 'addVaccine.html', {"form": form})
    


def addSchedule(request):
    if not request.user.is_authenticated:
        return redirect("homepage")
    
    if not request.user.account.is_doctor:
        messages.error(request, "As a patient you can't add schedule") #todo patient can't add schedule
        return redirect("homepage")

    # vaccines = Vaccine.objects.filter(doctor = request.user.account) # we will filter from all vaccine
    # print("vaccines objects are :", vaccines)
    if request.method == "POST":
        
        form = AddScheduleForm(request.POST, doctor = request.user.account)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = AddScheduleForm(doctor = request.user.account)
        
    return render(request, 'schedule.html', {"form":form, 'type':"Add Schedule Form", "button": "update"})
    



class AddScheduleView(CreateView):
    template_name = 'schedule.html'        
    form_class = AddScheduleForm
    model = Schedule
    test_data = None


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = self.request.user.account 
        print("kwargs :", kwargs)
        return kwargs
        #todo Pass user as kwargs so that we can apply that a doctor can add schedule for his/her added vaccines
    

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Schedule added successfully!")
        return reverse_lazy("profile")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Add Schedule Form'
         
        context['form'] = self.form_class   
        return context





def editSchedule(request,id):
    if request.method == 'POST':
        schedule = Schedule.objects.get(id = id)

        form = AddScheduleForm(request.POST, instance=schedule)

        if form.is_valid():
            form.save()
            messages.success(request, "Schedule update successfully!")

            return redirect("profile")
    else:
        form = AddScheduleForm(instance= Schedule.objects.get(id = id))
    return render(request, "editSchedule.html", {"form":form, "type":"Edit Schedule Form"})



def deleteSchedule(request, id):
    schedule = None
    try:
        schedule = Schedule.objects.get(id = id)
        schedule.delete()
        messages.info(request, "Schedule delete successfully!")
    except:
        messages.error(request, "This schedule does not exist.")
    return redirect("homepage")



class BookDose(CreateView):
    template_name = "book_dose.html"
    form_class = BookDoseForm
    # success_message = 'Dose Booked Successfully!'
    model = Vaccine_Recipient
    

    def get_success_url(self):
        return reverse_lazy("profile")
    
  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter() # Todo apply filter
        return queryset
    
    def form_valid(self, form):
        dose = form.save(commit = False)
        dose.account = self.request.user.account
        # dose.next_dose = form.cleaned_data.get('schedule')
        # dose.save()
        
        dose.next_dose = dose.schedule.date +  timedelta(days = 7)
       
        dose.save()
        # first time save na korla tar satha schedule er ja relationship kora chilo
        messages.success(self.request, "Dose Book Successfully!")

        return HttpResponseRedirect(self.get_success_url())
        
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Something is wrong!")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = self.form_class

        return context
    
    

def vacDetails(request, id):
    vaccine =  Vaccine.objects.get(id = id)
    hasAdded = False
    try:
        if vaccine.doctor == request.user.account:
            hasAdded = True
        else:
            hasAdded = False
    except:
        hasAdded = False
    schedules = Schedule.objects.filter(vaccine = vaccine)
    reviews = Review.objects.filter(vaccine = vaccine)

    recipient = None
    canGiveReview = True
    if request.user.is_authenticated :
        # corner case
            # user may not take that vaccine
            # user have already reviewed for that vaccine
        recipient = Vaccine_Recipient.objects.filter(account = request.user.account, vaccine = vaccine)
        print("recipient object",recipient)

        if len(recipient) == 0 or len(recipient) >= 2: # user must have Vaccine_Recipient instance
            canGiveReview = False
        
        singleRecipient = None
        for rec in recipient:
            singleRecipient = rec
            break
        isReviewed = Review.objects.filter(vaccine = vaccine, reviewer = singleRecipient)

        if len(isReviewed):
            canGiveReview = False
        
        




    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "You can't add review as an anonymous user")
            return redirect("login")

        form = ReviewForm(request.POST)
        if form.is_valid:
            review = form.save(commit = False)
            recipient = Vaccine_Recipient.objects.filter(account = request.user.account, vaccine = vaccine)
            if len(recipient) > 0:
                recipient  = recipient[0]
            else:
                recipient = None



            review.reviewer = recipient
            review.vaccine = vaccine
            review.save()
            messages.success(request, "Review Added Successfully!")
            return redirect("vacDetails", id)

    else:
        form = ReviewForm()
    return render(request, 'vacDetails.html', {"vaccine": vaccine, 'form': form, 'reviews': reviews, "schedules": schedules, 'hasAdded': hasAdded, "recipient": recipient, 'canGiveReview': canGiveReview})

    
    
    
    





def your_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
        form = AddScheduleForm(user=request.user, doctor=doctor)