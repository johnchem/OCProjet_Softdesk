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
        on_delete=models.DO_NOTHING,
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
        on_delete=models.DO_NOTHING,
        related_name="responsible_of",
        # default='',
    )
    created_time = models.DateTimeField(
        auto_now_add=True
    )


class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = "__all__"
