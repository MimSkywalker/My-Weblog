
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
   path('', views.blog_view, name='blog'),
   path('category/<slug:cat_slug>/', views.blog_view, name='category'),
   path("tag/<slug:tag_slug>/", views.blog_view, name="tag"),
]
