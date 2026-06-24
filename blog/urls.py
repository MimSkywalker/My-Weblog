
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_view, name='blog'),
    path('category/<slug:cat_slug>/', views.blog_view, name='category'),
    path("tag/<str:tag_slug>/", views.blog_view, name="tag"),
    path("post/<slug:slug>/", views.single_post_view, name="single_post"),
    path('manage/posts/', views.AdminPostListView.as_view(), name='admin_post_list'),
    path('manage/posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('manage/post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('manage/category/quick-create/', views.quick_category_create, name='quick_category_create'),


]
