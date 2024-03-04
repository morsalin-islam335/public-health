from django.contrib import admin

# Register your models here.
from . models import Vaccine, Schedule, Review, Vaccine_Recipient


admin.site.register(Vaccine)
admin.site.register(Schedule)
admin.site.register(Review)
admin.site.register(Vaccine_Recipient)