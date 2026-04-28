from token import TILDE
from turtle import title
from urllib import request

from django.shortcuts import render, redirect
from blog.models import Post
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from .forms import ContactMessageForm
from django.shortcuts import get_object_or_404
from django.db.models import Q



User = get_user_model()

def homepage(request):
    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED,
        published_at__isnull=False
    ).order_by("-published_at")
    mohammad = User.objects.get(username="mohammad")
    paginator = Paginator(posts, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"posts":page_obj, "mohammad":mohammad, "page_obj": page_obj,}
    return render(request, "home/index.html",context)



def about_view(request):
    mohammad = User.objects.get(username="mohammad")
    context = {"mohammad":mohammad}
    return render(request, "home/about.html", context)


def contact_view(request):
    form = ContactMessageForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پیام شما با موفقیت ثبت شد. ممنون از شما!")
        return redirect("home:contact")

    if request.method == "POST":
        messages.error(request, "فرم نامعتبر است. لطفاً ورودی‌ها را بررسی کنید.")

    mohammad = User.objects.filter(username="mohammad").first()

    context = {
        "form": form,
        "mohammad": mohammad,
    }
    return render(request, "home/contact.html", context)



def projects_view(request):
    mohammad = User.objects.get(username="mohammad")
    context = {"mohammad":mohammad}
    return render(request, "home/projects.html", context)


def home_search(request):
    mohammad = User.objects.get(username="mohammad")
    posts = Post.objects.filter(
    status=Post.Status.PUBLISHED,
    published_at__isnull=False
    ).order_by("-published_at")

    if request.method == "GET":
        if q := request.GET.get('q'):
            posts= posts.filter(
                Q(content__icontains=q)|
                Q(title__icontains=q)|
                Q(title_en__icontains=q)|
                Q(excerpt__icontains=q)            
                )
    context = {'posts': posts, "mohammad":mohammad}
    return render(request, 'home/index.html', context)
    