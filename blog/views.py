
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Post, Category


User = get_user_model()

def blog_view(request, cat_slug=None, tag_slug=None):
    categories = Category.objects.all()
    posts = Post.objects.filter(status = Post.Status.PUBLISHED).order_by('-published_at')
    mohammad = User.objects.get(username="mohammad")

    if cat_slug:
        posts = posts.filter(category__slug = cat_slug)

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    context = {"posts" : posts,
               "categories": categories,
               "mohammad": mohammad,
                "active_category": cat_slug,
                }
    return render(request, 'blog/blog.html', context)