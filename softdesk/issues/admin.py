from django.contrib import admin
from django import forms
from django.contrib import admin
from issues.models import Issues

# Register your models here.

class IssuesForm(forms.ModelForm):
    class Meta:
        model=Issues
        fields=["title", "desc", "tag", "priority", "status", "project_id", "assignee_user_id"]

@admin.register(Issues)
class IssuesAdmin(admin.ModelAdmin):
    class Meta:
        form=IssuesForm
        list_display=("issues_id", "title", "project_id", "assignee")