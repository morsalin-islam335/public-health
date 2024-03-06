from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from .forms import Registration, UpdateProfile
from django.contrib.auth.models import User 
from . models import Account
from vaccine.models import Vaccine, Vaccine_Recipient
from django.contrib import messages
from django.contrib.auth import login, logout

# email send process

from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string


# verification mail korar jonno

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

def registration(request, isDoctor = None):  # We work both doctor and patient role in same views
    if request.user.is_authenticated:
        return redirect("profile") # a log in user can't register with out logout
    if request.method == 'POST':
        form = Registration(request.POST, request.FILES)
        if form.is_valid():
            # form.save()

            #  set user
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            profile_pic = form.cleaned_data.get("profile_pic")
            nid = form.cleaned_data.get("nid")


            user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)


           

            user.set_password(password)
            user.is_active = False
            user.save()
            user = User.objects.get(username = username)
           
            if isDoctor:
                account = Account(user=user, profile_pic=profile_pic, nid = nid, is_patient = True) # doctor also can book a vaccine from another doctor's added vaccine 
                #todo when admin approve as doctor a verification link will be sent to his account
                account.save()
                messages.success(request, "Your Account has created successfully!  Wait for approval link till admin approve you.")

            else:
                account = Account(user=user, profile_pic=profile_pic, nid = nid, is_patient = True) 
                account.save()
                    
                token = default_token_generator.make_token(user) # user er jonno token generate korba
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                conform_link = f"https://public-health.onrender.com/account/activate/{uid}/{token}"
                # conform_link = f"http://127.0.0.1:8000//account/activate/{uid}/{token}"



                mail_subject = "Account Verification Mail"
                message = render_to_string("verificationMail.html", {"conform_link": conform_link})

                to_email = email

                send_message = EmailMultiAlternatives(mail_subject, "", to = [to_email])

                send_message.attach_alternative(message, 'text/html')

                send_message.send()
                

                messages.success(request, "Registration Complete. Please Check your email for conformation email")
            
          
            return redirect("homepage")
        

    else:
        form = Registration(request.POST, request.FILES)
    return render(request, 'register.html', {"form": form, "type": "Sign-Up"})
    



def userUpdateProfile(request):
    if request.method == "POST":
        # account = Account.objects.get(user = request.user)
        user = request.user
        form = UpdateProfile(request.POST, request.FILES, instance = user)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password")
            profile_pic = form.cleaned_data.get("profile_pic")
            nid = form.cleaned_data.get("nid")

            user = request.user
            account = Account.objects.get(user = user)

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            
            
            user.save()
            update_session_auth_hash(request, user)



            account.user = user  # ek bar user update korar por abar o set korta hoiba
            account.profile_pic = profile_pic
            account.nid = nid

            account.save()

            messages.success(request, "Account update successfully!")
            return redirect("profile")
    else:
        user = request.user
        form = UpdateProfile(instance = user)
    return render(request, "register.html", {"form":form , "type": "Update-Profile"})
    
        





         




class LoginView(LoginView):
    template_name = 'login.html'
    # form class nia kaj korar ei lagba na
    def get_success_url(self):
        return reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, 'Login Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Login Information incorrect")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
       
        return context
    

def UserLogout(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    messages.info(request, 'logout successfully')
    return redirect("homepage")


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "You can't go Profile page as a anonymous user")
        return redirect("login")
    
    isDoctor = None
    try:
        if request.user.account.is_doctor:
            isDoctor = True
    except:
        isDoctor = None

    addedVaccine = None

    try:
        if isDoctor:
            addedVaccine = Vaccine.objects.filter(doctor = request.user.account)
    except:
        addedVaccine = None

    bookDoses = Vaccine_Recipient.objects.filter(account = request.user.account)
    length = len(bookDoses)
    # all_dose_date = None
    # if length:
    #     dose_campaign_date = dict() # specific dose may have multiple date
    #     for dose in bookDoses:
    #         for i in range (1, dose.vaccine.total_dose+1):
    #             dose_campaign_date[dose] = f"Campaign {1} Date: {dose.vaccine}"
    return render(request, 'profile.html', {"addedVaccine": addedVaccine, 'length': length, 'bookDoses': bookDoses, "isDoctor":isDoctor})






def changePassword(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST) # user and method

        if form.is_valid():
            user = form.save() # just catch user
            update_session_auth_hash(request, user=user)

            messages.info(request, "Password Change Successfully!")

        return redirect("profile")
    
    else:
        form = PasswordChangeForm(request.user) #kon user er password change korba seta parenthesis er vitor a bola dita hoba
    
    return render(request, 'changePass.html', {"form": form})





def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk = uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        return redirect("login")
    else:
        messages.error(request, "Something is wrong.")
        return redirect("homepage")
    

def conformationForDeleteAccount(request):
    if not request.user.is_authenticated:
        messages.error(request, "You can't delete any account as an anonymous user")

        return redirect("login")
    else:
        return render(request, "conformationForDeleteAccount.html")
  

    
def deleteAccount(request):
    if not request.user.is_authenticated:
        messages.error(request, "You can not delete any account as an anonymous user")
        return redirect("login")
    
    user = request.user
    logout(request)

    user.delete()
    messages.info(request, "Account Delete Successfully!")

    return redirect("homepage")
