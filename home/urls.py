
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
   path("",views.homepage, name="homepage"),
   path("about/",views.about_view, name="about"),
   path("contact/",views.contact_view, name="contact"),
   path("projects/",views.projects_view, name="projects"),
]
