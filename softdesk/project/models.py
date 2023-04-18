from django.db import models
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


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="A")


class ContributorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="C")
    
class ResponsibleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role="R")

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    type = models.CharField(
        max_length=5,
        choices=TYPE_PROJECT,
        )
    
    @property
    def author_user_id(self):
        queryset = User.objects.filter(contributor__project_id=self.project_id)
        
        return queryset.data


class Contributor(models.Model):
    user_id = models.ForeignKey(
        to=User, 
        related_name="contributor", 
        on_delete=models.CASCADE,
        to_field="user_id"
        )
    project_id = models.ForeignKey(
        to=Project,
        related_name="project",
        on_delete=models.CASCADE,
        to_field="project_id"
    )
    role = models.CharField(
        max_length=1,
        choices=FUNCTION,
        default=CONTRIBUTOR,
    )

    class Meta:
        unique_together = ('user_id', 'project_id')