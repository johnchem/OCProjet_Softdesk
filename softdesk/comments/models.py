from django.db import models

from authentification.models import User
from issues.models import Issues

from rest_framework import serializers

# Create your models here.


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=256)
    author_user_id = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="comment",
        related_query_name="comments"
    )
    issues_id = models.ForeignKey(
        to=Issues,
        on_delete=models.CASCADE,
        related_name="comment",
        related_query_name="comments"
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = (
            "comment_id",
            "issues_id",
            "description",
            "author_user_id",
            "created_time",
        )

    def __str__(self):
        return f"#{self.comment_id} - {self.author_user_id} : {self.description}"
