
from . import views
from django.urls import path, include


app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),


]
