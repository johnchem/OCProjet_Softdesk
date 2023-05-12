from django.db import models

from project.models import Project
from authentification.models import User


class Issues(models.Model):
    issues_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=64)
    desc=models.CharField(max_length=256)
    tag=models.CharField(max_length=128)
    priority=models.CharField(max_length=32)
    project_id=models.ForeignKey(
        to=Project,
        on_delete=models.DO_NOTHING
    )
    status=models.CharField(max_length=32)
    author_user_id=models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="issue_author"
    )
    assignee_user_id=models.ManyToManyField(
        to=User,
        related_name="responsible"
    )
    created_time=models.DateTimeField(
        auto_now_add=True
    )

