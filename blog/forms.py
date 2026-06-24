

from django import forms
from blog.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "subject", "message"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['featured_image', 'title', 'title_en','slug',
                  'status', 'excerpt', 'content', 'category', 'tags', 'meta_description', 'login_required', 'published_at']

        read_only_fields = ['id', 'created_at', 'updated_at',]