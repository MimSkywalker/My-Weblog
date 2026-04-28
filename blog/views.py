
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from taggit.models import Tag

User = get_user_model()

def blog_view(request, cat_slug=None, tag_slug=None):
    categories = Category.objects.all()
    mohammad = User.objects.get(username="mohammad")
    tags = Tag.objects.all()

    posts = Post.objects.filter(status = Post.Status.PUBLISHED).order_by('-published_at')
    active_category = None
    active_tag = None
    if cat_slug:
        posts = posts.filter(category__slug = cat_slug)
        active_category = cat_slug

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
        active_tag = tag_slug

    context = {"posts" : posts,
               "categories": categories,
               "tags": tags,
               "mohammad": mohammad,
                "active_category": active_category,
                "active_tag":active_tag,
                }
    return render(request, 'blog/blog.html', context)



def single_post_view(request, slug):

        post = get_object_or_404(Post, slug=slug)
        mohammad = User.objects.get(username="mohammad")
        context={"post":post, "mohammad":mohammad}
        return render(request, 'blog/single_post.html', context)