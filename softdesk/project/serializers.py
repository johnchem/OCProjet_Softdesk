from rest_framework import serializers

from authentification.models import User
from project.models import Contributor, Project, TYPE_PROJECT

class ContributorSerializer(serializers.ModelSerializer):
    Permission = serializers.CharField()
    class Meta:
        models = Contributor
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
    role = serializers.ChoiceField(
        choices=TYPE_PROJECT,
        style={'base_template':'radio.html'}
    )
    # author_user_id = serializers.SerializerMethodField()

    class Meta:
        models = Project
        fields = ['project_id', 'title', 'description', 'type']


    # def create_project(self, author_id):
    #     project = Project(
    #         title = self.validated_data['title'],
    #         description = self.validated_data['description'],
    #         type = self.validated_data['type'],
    #         author_user_id = author_id,
    #     )
    #     project.save()

