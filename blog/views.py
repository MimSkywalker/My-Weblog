

from django.contrib import messages
from django.db.models.query import QuerySet
from django.utils import timezone

from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Category, Comment
from taggit.models import Tag
from blog.forms import CommentForm, PostForm

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.text import slugify

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test


def blog_view(request, cat_slug=None, tag_slug=None):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    posts = Post.objects.filter(
        status=Post.Status.PUBLISHED,
        published_at__lte=timezone.now()
    ).select_related('category').order_by('-published_at')
    active_category = None
    active_tag = None
    if cat_slug:
        posts = posts.filter(category__slug=cat_slug)
        active_category = cat_slug

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
        active_tag = tag_slug

    context = {"posts": posts,
               "categories": categories,
               "tags": tags,
               "active_category": active_category,
               "active_tag": active_tag,
               }
    return render(request, 'blog/blog.html', context)


def single_post_view(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status=Post.Status.PUBLISHED,
        published_at__lte=timezone.now()
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            
            if request.user.is_authenticated:
                comment.name = request.user.get_full_name() or request.user.username
                comment.email = request.user.email

            else:
                if not comment.name or not comment.email:
                    messages.error(request, "کاربران مهمان باید نام و ایمیل خود را وارد کنند.")                
                    comments = post.comments.filter(is_approved=True).select_related('post')
                    context = {"post": post, "comments": comments, "form": form}
                    return render(request, 'blog/single_post.html', context)


            comment.save()


            messages.success(
                request, "دیدگاه شما با موفقیت ثبت شد. سپاس‌گزارم!")
            return redirect("blog:single_post", slug=slug)

        else:
            messages.error(
                request, "فرم نامعتبر است. لطفاً ورودی‌ها را بررسی کنید.")
    else:
        form = CommentForm()

    comments = post.comments.filter(is_approved=True).select_related('post')

    context = {"post": post, "comments": comments, "form": form, }
    return render(request, 'blog/single_post.html', context)


class AdminPostListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = 'blog/admin/admin_post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    paginate_orphans = 7

    def get_queryset(self):
        return Post.objects.select_related('category').prefetch_related('tags').all().order_by('-created_at')

    def test_func(self):
        return self.request.user.is_superuser


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/admin/post_form.html'
    success_url = reverse_lazy('blog:admin_post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


@login_required
@user_passes_test(lambda u: u.is_superuser)
def quick_category_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title_fa = data.get('title')
            title_en = data.get('title_en')

            if title_fa and title_en:
                generated_slug = slugify(title_en)

                if Category.objects.filter(slug=generated_slug).exists():
                    return JsonResponse({'success': False, 'error': 'دسته‌بندی با این عنوان انگلیسی از قبل وجود دارد.'})

                new_category = Category.objects.create(
                    title=title_fa,
                    title_en=title_en,
                    slug=generated_slug
                )

                return JsonResponse({
                    'success': True,
                    'id': new_category.pk,
                    'title': new_category.title
                })

            return JsonResponse({'success': False, 'error': 'فیلدها نباید خالی باشند.'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر است.'})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/admin/post_form.html'
    success_url = reverse_lazy('blog:admin_post_list')

    def test_func(self):
        return self.request.user.is_superuser


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:admin_post_list')
    template_name = 'blog/admin/post_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser
