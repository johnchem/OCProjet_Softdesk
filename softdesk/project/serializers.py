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
    
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id']
        
    def create(self, validated_data):
        return Project.objects.create(**validated_data)
