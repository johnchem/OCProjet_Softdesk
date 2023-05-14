from django.db import models

from authentification.models import User
from issues.models import Issues

# Create your models here.

class Comments(models.Model):
    comment_id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=256)
    author_user_id=models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="comment",
        related_query_name="comments"
    )
    issues_id=models.ForeignKey(
        to=Issues,
        on_delete=models.CASCADE,
        related_name="comment",
        related_query_name="comments"
    )
    created_time=models.DateTimeField(
        auto_now_add=True
    )