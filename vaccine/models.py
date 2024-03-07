from django.db import models

# Create your models here.
from account . models import Account




class Vaccine(models.Model):
    name = models.CharField(max_length = 40)
    doctor = models.ForeignKey(Account, on_delete = models.CASCADE, null = True, blank = True, related_name = "vaccines") # a doctor can add multiple vaccine
    total_dose = models.IntegerField(null = True, blank = True)

    dose = models.IntegerField()
    price = models.IntegerField()
    # next_dose = models.DateField(null = True, blank = True) # ei field ta nia apato to kaj nei. 
    description = models.TextField(max_length = 600)
    image = models.ImageField(upload_to= 'vaccine/upload/images/')
    

    def __str__(self):
        return f"Vaccine : {self.name}"



class Schedule(models.Model):
    date =  models.DateField()
    vaccine = models.ForeignKey(Vaccine, on_delete = models.CASCADE, related_name = 'schedules')
    # a vaccine may have multiple schedule

    def __str__(self):
        return f"{self.vaccine} schedule: {self.date}"


star  = [
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]

class Vaccine_Recipient(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE, null = True, blank = True, related_name = 'recipient')
    vaccine = models.ForeignKey(Vaccine,on_delete = models.CASCADE, related_name = 'receiver', null = True, blank = True) # an receiver an take multiple vaccine
    schedule = models.OneToOneField(Schedule,  on_delete = models.CASCADE, related_name = "recipients")
    hasReviewed = models.BooleanField(default = False) # that will be track if an user are already reviewed or not for a specific vaccine or not
    taken_dose = models.IntegerField(default = 0)
    next_dose = models.DateField(null = True, blank = True) # eta dia next dose koba ta show korbo
    is_complete_dose = models.BooleanField(default = False)


    def __str__(self):
        return f"{self.account}"


from account.models import Account
class Review(models.Model):
    star = models.CharField(max_length = 10, choices = star)
    review = models.TextField()
    reviewer = models.ForeignKey(Vaccine_Recipient, null = True, blank = True, related_name = "review", on_delete = models.CASCADE) #a receiver can give multiple review

    vaccine = models.ForeignKey(Vaccine, on_delete = models.CASCADE, null = True, blank = True) # a vaccine may have multiple review




    def __str__(self):
        return f"star : {self.star}"





