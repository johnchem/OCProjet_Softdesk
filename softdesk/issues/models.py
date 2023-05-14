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
        on_delete=models.DO_NOTHING,
        related_name="issue",
        related_query_name="issues"
    )
    status=models.CharField(max_length=32)
    author_user_id=models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="issues_created"
    )
    assignee_user_id=models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="responsible_of",
        default='',
    )
    created_time=models.DateTimeField(
        auto_now_add=True
    )

