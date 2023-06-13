from django.contrib import admin
from django import forms
from comments.models import Comments

# Register your models here.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = "__all__"


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    form = CommentForm
    list_display = ["comment_id", "description", "author_user_id", "issues_id"]
