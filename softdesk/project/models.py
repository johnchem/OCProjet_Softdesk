from django.db import models
from rest_framework import serializers

from authentification.models import User

# Create your models here.
WEB_BACK = 'BACK'
WEB_FONT = 'FRONT'
MOBILE_IOS = 'IOS'
MOBILE_ANDROID = 'ANDRD'

AUTHOR = "A"
RESPONSIBLE = "R"
CONTRIBUTOR = "C"

FUNCTION = [
    (AUTHOR, 'author'),
    (RESPONSIBLE, 'responsible'),
    (CONTRIBUTOR, 'contributor'),
]

TYPE_PROJECT = [
    (WEB_BACK,'back-end'), 
    (WEB_FONT,'front-end'),
    (MOBILE_IOS,'iOS'),
    (MOBILE_ANDROID,'Android'),
]

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    type = models.CharField(
        max_length=5,
        choices=TYPE_PROJECT,
        )
    author_user_id = models.ForeignKey(
        to=User,
        related_name="project_created",
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    
    def __str__(self):
        return f"{self.title} - {self.author_user_id}"


class Contributor(models.Model):
    user_id = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        related_name="member_of"
        )
    project_id = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="contributor"
        )
    role = models.CharField(
        max_length=1,
        choices=FUNCTION,
        default=CONTRIBUTOR,
    )

    class Meta:
        unique_together = ('user_id', 'project_id')

class ContributorSerializer(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField('get_permission')
    
    # project = ProjectSerializer()
    
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'role', 'permission']

    def get_permission(self, instance):
        if instance.role == "A":
            return "CRUD"
        if instance.role == "R":
            return "RU"
        if instance.role == "C":
            return "R"


class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=TYPE_PROJECT,
        style={'base_template':'radio.html'}
    )

    contributor = ContributorSerializer(many=True)
    
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'contributor']

    def create(self, validated_data):
        author = self.context['request'].user
        project = Project.objects.create(
            author_user_id=author,
            **validated_data
            )
        return project
