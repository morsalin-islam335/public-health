from django.urls import path


from . views import home, about, services
urlpatterns = [
    path("", home, name = 'homepage'),
    path("about/",about, name = 'about'),
    path("services/",services, name = 'services'),
]
