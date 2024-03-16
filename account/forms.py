
from typing import Any
from django import forms
from django.contrib.auth.models import User
from . models import Account


from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox



class Registration(forms.ModelForm):

    username = forms.CharField(max_length= 30, label = 'user name', widget=forms.TextInput(attrs={"class":"form-field", "placeholder":"Enter your username"}))
    first_name = forms.CharField(max_length= 30, label = 'first name', widget=forms.TextInput(attrs={"class":"form-field", 'placeholder':'Enter Your First Name'}))
    last_name = forms.CharField(max_length= 30, label = 'last name', widget=forms.TextInput(attrs={"class":"form-field", 'placeholder':'Enter Your Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-field", 'placeholder':'Enter Your Email'}))

    conform_password = forms.CharField(max_length = 20, widget = forms.PasswordInput(attrs= {"class": "form-field", 'placeholder':'Conform Password'}), label = 'Confirm password')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs= {"class": "form-field", 'placeholder':'Enter a strong password'}))
    nid = forms.CharField(max_length=17, widget= forms.TextInput(attrs= {"class": "form-field", 'placeholder':'Enter Nid Number'}))
    profile_pic = forms.ImageField(widget = forms.FileInput(attrs= {"class": "form-field"}))
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'conform_password','nid', 'profile_pic', 'captcha'] #

 
    
    def clean(self):
        data = super().clean() # sob gulo data nilam
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("conform_password")
        nid = data.get("nid")
        email = data.get("email")

        # if password != password2:
        #     raise forms.ValidationError("Password and conform password are not same.")
        # if len(password) < 8:
        #     raise forms.ValidationError("Minimum 8 digits/char is required")

        if  Account.objects.filter(nid = nid).exists():
            raise forms.ValidationError("This Nid information is already exist")
        
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("This email is already exists!")


# class UpdateProfile(forms.ModelForm):
#     username = forms.CharField(max_length= 30, label = 'user name', widget=forms.TextInput(attrs={"class":"form-field"}))
#     first_name = forms.CharField(max_length= 30, label = 'first name', widget=forms.TextInput(attrs={"class":"form-field"}))
#     last_name = forms.CharField(max_length= 30, label = 'last name', widget=forms.TextInput(attrs={"class":"form-field"}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-field"}))
#     nid = forms.CharField(max_length=17, widget= forms.TextInput(attrs= {"class": "form-field"}))
#     profile_pic = forms.ImageField()

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']

    
#     def clean(self):
#         data = super().clean() # sob gulo data nilam

#         nid = data.get("nid")
#         if  Account.objects.filter(nid = nid).exists():
#             raise forms.ValidationError("This Nid information is already exist")
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         if self.instance:
#             try:
#                 user = self.instance
                
#                 account = self.instance.account
#             except:
#                 account = None
#                 user = None
#             if account:
#                 self.fields['username'].initial = user.username
#                 self.fields['first_name'].initial = user.first_name
#                 # self.fields['last_name'].initial = user.last_name
#                 # self.fields['email'].initial = user.email
#                 # self.fields['nid'].initial = user.account.nid
#                 # self.fields['profile_pic'] = user.account.profile_pic


        
class UpdateProfile(forms.ModelForm):

    nid = forms.CharField(max_length=17, widget= forms.TextInput(attrs= {"class": "form-field"}))
    profile_pic = forms.ImageField()
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       

        # jodi user er account thake 
        if self.instance:
            try:
                account = self.instance.account
                
            except:
                account = None
               

            if account:
                self.fields['nid'].initial = account.nid
                self.fields['profile_pic'].initial = account.profile_pic
    
    def clean(self) -> dict[str, Any]:
        data = super().clean()

        nid = data.get("nid")
        email = data.get("email")

        # nidWithAssociatedAccount = Account.objects.filter(nid = nid) # first time ti will be check if this nid is common or not
        # if nidWithAssociatedAccount: # if that nid is common then ...
        #     nidWithAssociatedAccount = Account.objects.get(nid = nid) # catch this nid
        #     if nidWithAssociatedAccount.user.email != self.instance.account.email:
        #         raise forms.ValidationError("This Nid is already taken")
        ''' Django model will handle before logics as unique = True'''

        emailWithAssociatedAccount = Account.objects.filter(email = email) # first time ti will be check if this email is common or not
        if emailWithAssociatedAccount: # if that email is common then ...
            emailWithAssociatedAccount = Account.objects.get(user = User.objects.get(email = email)) # catch this email
            if emailWithAssociatedAccount.user.email != self.instance.account.email:
                raise forms.ValidationError("This Nid is already taken")


        
# class UpdateProfile(forms.ModelForm):

#     nid = forms.CharField(max_length=17, widget= forms.TextInput(attrs= {"class": "form-field"}))
#     profile_pic = forms.ImageField()
    

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',  'email']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
       

#         # jodi user er account thake 
#         if self.instance:
#             try:
#                 account = self.instance.account
                
#             except:
#                 account = None
               

#             if account:
#                 self.fields['nid'].initial = account.nid
#                 self.fields['profile_pic'].initial = account.profile_pic
    
#     def clean(self) -> dict[str, Any]:
#         data = super().clean()



class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs= {"class": "form-field"}), label= "Email")
    password = forms.CharField(max_length=20, widget= forms.PasswordInput(attrs = {"class": 'form-field'}), label= 'Password')

    captcha = ReCaptchaField(label = "Captcha")    