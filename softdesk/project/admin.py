from django import forms
from django.contrib import admin
from project.models import Project, Contributor

# Register your models here.
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "type", "author_user_id"]
        
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm

admin.site.register(Project)
admin.site.register(Contributor)