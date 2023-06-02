from django import forms
from django.contrib import admin
from project.models import Project, Contributor

# Register your models here.
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "type", "author_user_id"]

class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['user_id']
        
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('project_id', 'title', 'author_user_id')

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    form = ContributorForm
    list_display = ('user_id', 'project_id', 'role')

# admin.site.register(Project)
# admin.site.register(Contributor)