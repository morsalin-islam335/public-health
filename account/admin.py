from django.contrib import admin

# Register your models here.


#todo Email send packages

from django.contrib.auth.tokens import default_token_generator # todo generate token for user
from django.core.mail import EmailMultiAlternatives #todo sent mail
from django.template.loader import render_to_string #todo render html to string as email
from django.utils.encoding import force_bytes # todo encode user token
from django.utils.http import urlsafe_base64_encode # todo encode user token so that  that will provide extra security



from . models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'nid']


    def username(self, obj):
        return f"{obj.user.username}"
    
    def first_name(self, obj):
        return f"{obj.user.first_name}"

    def last_name(self, obj):
        return f"{obj.user.last_name}"

    def email(self, obj):
        return f"{obj.user.email}"
    
    def save_model(self, request, obj, form, change):
        
        obj.save()
        user = obj.user
       
        if obj.is_doctor == True: #todo check if is_patient true or not
           
            token = default_token_generator.make_token(user) # user er jonno token generate korba
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            conform_link = f"http://127.0.0.1:8000//account/activate/{uid}/{token}"
            # conform_link = f"https://spread-knowledge.onrender.com/account/activate/{uid}/{token}"



            mail_subject = "Admin Approval and Account Activation Email"
            message = render_to_string("verification_as_adminMail.html", {"conform_link": conform_link})

            to_email = user.email

            send_message = EmailMultiAlternatives(mail_subject, "", to = [to_email])

            send_message.attach_alternative(message, 'text/html')

            send_message.send()
            

        

    


admin.site.register(Account, AccountAdmin)
