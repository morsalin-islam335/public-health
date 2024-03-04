from typing import Iterable
from django.db import models


# Create your models here.




from django.contrib.auth.models import User
class Account(models.Model):
    user = models.OneToOneField(User, related_name = 'account', on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to="account/upload/images/")
    nid = models.CharField(max_length = 17, unique = True)
    is_doctor = models.BooleanField(default = False)
    is_patient = models.BooleanField(default = False)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
