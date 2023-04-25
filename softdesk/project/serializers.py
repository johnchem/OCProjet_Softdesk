from rest_framework import serializers

from authentification.models import User
from authentification.serializers import UserSerializer

from project.models import Contributor, Project, TYPE_PROJECT
from project.models import AUTHOR


class ContributorSerializer(serializers.ModelSerializer):
    Permission = serializers.CharField()
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']
    
    
    def add_contributor(self, project_id, email, role):
        user = User.objects.filter(email = email)
        contributor = Contributor(
            user_id = user['user_id'],
            project_id = project_id,
            role = self.validated_data['role']
            )
        contributor.save()

class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=TYPE_PROJECT,
        style={'base_template':'radio.html'}
    )
    author_user_id = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id']

    def get_author_user_id(self, instance):
        queryset = Contributor.objects.filter(project_id=instance.project_id)
        q1 = list(queryset.filter(role=AUTHOR))
        author = q1[0]
        serializers = UserSerializer(author.user_id)

        return serializers.data
        


    # def create_project(self, author_id):
    #     project = Project(
    #         title = self.validated_data['title'],
    #         description = self.validated_data['description'],
    #         type = self.validated_data['type'],
    #         author_user_id = author_id,
    #     )
    #     project.save()

