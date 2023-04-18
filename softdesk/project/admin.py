from django.contrib import admin
from project.models import Project, Contributor

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    fields = ["project_id", "title", "description", "author_user_id"]

admin.site.register(Project)
admin.site.register(Contributor)