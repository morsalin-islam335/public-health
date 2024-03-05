from typing import Any
from django import forms 

from .models import Vaccine,Schedule, Vaccine_Recipient, Review


class addVaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = ["name",'total_dose','price', 'description','image' ]
    


    # def save(self, commit = True) :
    #     vaccine = super().save(commit = False)
    #     vaccine.dose = self.cleaned_data.get("total_dose")
    #     vaccine.save()



        




  
class AddScheduleForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput({"type": "date"}))

    # def __init__(self, *args, **kwargs):
    #     doctor = kwargs.pop('doctor', None)  # Retrieve the user from kwargs
    #     super().__init__(*args, **kwargs)
    #     if doctor:
    #         self.fields['vaccine'].queryset = Vaccine.objects.filter(doctor = doctor)
    #         print("vaccine are ", Vaccine.objects.filter(doctor = doctor))
    #         print("doctor is :", doctor.user.username)


    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['vaccine'].queryset = Vaccine.objects.filter(doctor = doctor)
            print("vaccine are ", Vaccine.objects.filter(doctor = doctor))
            print("doctor is :", doctor.user.username)


    class Meta:
        model = Schedule
        fields = ['date', 'vaccine']


class BookDoseForm(forms.ModelForm):
    class Meta:
        model = Vaccine_Recipient
        fields = ['vaccine', 'schedule']
    
    # def save(self, commit = True):
    #     dose = super().save(commit = False)

    #     dose.account = self.instance.account

    #     dose.save()

        



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields= ['star', 'review']