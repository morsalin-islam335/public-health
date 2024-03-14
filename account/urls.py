from django.urls import path 

from . views import registration,UserLogin, LoginView, profile, userUpdateProfile, changePassword, profile, UserLogout, activate, conformationForDeleteAccount, deleteAccount

urlpatterns = [
    path("doctor/registration/<int:isDoctor>", registration, name = 'register_as_doctor' ),
    path("patient/registration", registration, name = 'register_as_patient'),
    path("activate/<uid64>/<token>", activate, name = 'active'),
    # path("login/", LoginView.as_view(), name = 'login'),
    path("login/", UserLogin, name = 'login'),
    path("logout", UserLogout, name = 'logout'),
    # path("patient/profile"),
    path("updateProfile", userUpdateProfile, name = 'updateProfile'),
    path("deleteAccount", conformationForDeleteAccount , name = 'deleteAccount'),
    path("conformDelete", deleteAccount , name = 'conformDelete'),
   
    path("changePassword", changePassword, name = 'changePassword'),

    path("profile", profile, name = 'profile'),
    

]
