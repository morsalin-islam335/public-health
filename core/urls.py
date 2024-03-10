from django.urls import path


from . views import home, about, services, contact
urlpatterns = [
    path("", home, name = 'homepage'),
    path("about/",about, name = 'about'),
    path("services/",services, name = 'services'),
    path("contact/",contact, name = 'contact')
]
