

from django.contrib import messages

from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Category, Comment
from taggit.models import Tag
from blog.forms import CommentForm

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

    
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "دیدگاه شما با موفقیت ثبت شد. سپاس‌گزارم!")
            return redirect("blog:single_post", slug=slug)

        else:
            messages.error(request, "فرم نامعتبر است. لطفاً ورودی‌ها را بررسی کنید.")
    else:
        form = CommentForm()
    
    comments = post.comments.filter(is_approved=True)
    mohammad = User.objects.get(username="mohammad")

    context={"post":post, "mohammad":mohammad, "comments": comments, "form": form,}
    return render(request, 'blog/single_post.html', context)


