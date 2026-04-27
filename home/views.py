from django.shortcuts import render
from blog.models import Post
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

User = get_user_model()

def homepage(request):
    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED,
        published_at__isnull=False
    ).order_by("-published_at")
    
    mohammad = User.objects.get(username="mohammad")
    


    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"posts":page_obj, "mohammad":mohammad, "page_obj": page_obj,}
    return render(request, "home/index.html",context)