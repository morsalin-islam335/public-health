
from django import forms
from django.contrib.auth.models import User
from . models import Account


class Registration(forms.ModelForm):

    username = forms.CharField(max_length= 30, label = 'user name', widget=forms.TextInput(attrs={"class":"form-field"}))
    first_name = forms.CharField(max_length= 30, label = 'first name', widget=forms.TextInput(attrs={"class":"form-field"}))
    last_name = forms.CharField(max_length= 30, label = 'last name', widget=forms.TextInput(attrs={"class":"form-field"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-field"}))

    nid = forms.CharField(max_length=17, widget= forms.TextInput(attrs= {"class": "form-field"}))
    profile_pic = forms.ImageField(widget = forms.FileInput(attrs= {"class": "form-field"}))
    
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs= {"class": "form-field"}))
    conform_password = forms.CharField(max_length = 20, widget = forms.PasswordInput(attrs= {"class": "form-field"}), label = 'Confirm password')
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Password and conform password didn't match") # 2 ta password match na korla exception throw korbo
        
    
    def clean(self):
        data = super().clean() # sob gulo data nilam
        password = data.get("password")
        password2 = data.get("password2")
        nid = data.get("nid")

        if password and len(password) <8:
            raise forms.ValidationError("Minimum 8 digits is required")
        
        if  Account.objects.filter(nid = nid).exists():
            raise forms.ValidationError("This Nid information is already exist")
        


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
