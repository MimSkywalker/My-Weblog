from django.shortcuts import render, redirect
from blog.models import Post
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
from .forms import ContactMessageForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone


User = get_user_model()


def homepage(request):
    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED,
        published_at__lte=timezone.now()
    ).order_by("-published_at")
    paginator = Paginator(posts, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"posts": page_obj, "page_obj": page_obj, }
    return render(request, "home/index.html", context)


def about_view(request):
    return render(request, "home/about.html")


def contact_view(request):
    form = ContactMessageForm(request.POST or None)

    if request.user.is_authenticated:
        form.fields['name'].required = False
        form.fields['email'].required = False

    if request.method == "POST" and form.is_valid():

        contact_msg = form.save(commit=False)

        if request.user.is_authenticated:
            contact_msg.name = request.user.get_full_name() or request.user.username
            contact_msg.email = request.user.email
        else:
            # این چک الان معنی داره چون فیلدها required=False نیستن برای guest
            if not contact_msg.name or not contact_msg.email:
                messages.error(
                    request, "کاربران مهمان باید نام و ایمیل خود را وارد کنند.")
                return render(request, "home/contact.html", {"form": form})

        contact_msg.save()
        messages.success(request, "پیام شما با موفقیت ثبت شد. ممنون از شما!")
        return redirect("home:contact")

    if request.method == "POST":
        print(form.errors)
        messages.error(
            request, "فرم نامعتبر است. لطفاً ورودی‌ها را بررسی کنید.")

    return render(request, "home/contact.html", {"form": form})


def projects_view(request):
    return render(request, "home/projects.html")


def home_search(request):
    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED,
        published_at__lte=timezone.now()
    ).order_by("-published_at")

    if request.method == "GET":
        if q := request.GET.get('q'):
            posts = posts.filter(
                Q(content__icontains=q) |
                Q(title__icontains=q) |
                Q(title_en__icontains=q) |
                Q(excerpt__icontains=q)
            )
    context = {'posts': posts}
    return render(request, 'home/index.html', context)
