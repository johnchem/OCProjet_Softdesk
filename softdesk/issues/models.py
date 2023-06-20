from django.db import models
from rest_framework import serializers

from project.models import Project
from authentification.models import User

BUG = 'BUG'
AMELIORATION = 'AMELIORATION'
TACHE = 'TACHE'

LOW = 'FAIBLE'
MEDIUM = 'MOYENNE'
HIGH = 'ELEVEE'

TODO = 'A faire'
ONGOING = 'En cours'
DONE = 'Termine'

TAGS = [
    (BUG, 'BUG'),
    (AMELIORATION, 'AMELIORATION'),
    (TACHE, 'TACHE'),
]

PRIORITE = [
    (LOW, 'FAIBLE'),
    (MEDIUM, 'MOYENNE'),
    (HIGH, 'ELEVEE'),
]

STATUT = [
    (TODO, 'A faire'),
    (ONGOING, 'En cours'),
    (DONE, 'Termine'),
]


class Issues(models.Model):
    issues_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    tag = models.CharField(
        max_length=20,
        choices=TAGS,
        )
    priority = models.CharField(
        max_length=32,
        choices=PRIORITE,
        )
    project_id = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="issue",
        related_query_name="issues"
    )
    status = models.CharField(
        max_length=32,
        choices=STATUT,
        )
    author_user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="issues_created"
    )
    assignee_user_id = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        related_name="responsible_of",
        default=author_user_id,
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )


class IssuesSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H/%M/%S",
    )

    class Meta:
        model = Issues
        fields = [
            "issues_id",
            "project_id",
            "title",
            "desc",
            "tag",
            "priority",
            "status",
            "author_user_id",
            "assignee_user_id",
            "created_time"
            ]
