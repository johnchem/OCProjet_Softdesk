# from rest_framework import serializers

# from authentification.models import User
# from authentification.serializers import UserSerializer

# from project.models import Contributor, Project
# from project.models import AUTHOR, TYPE_PROJECT


# class ContributorSerializer(serializers.ModelSerializer):
#     permission = serializers.SerializerMethodField('get_permission')
#     class Meta:
#         model = Contributor
#         fields = ['user_id', 'project_id', 'role', 'permission']
        
#     def get_permission(self, instance):
#         if instance.role == "A":
#             return "CRUD"
#         if instance.role == "R":
#             return "RU"
#         if instance.role == "C":
#             return "R"


# class ProjectSerializer(serializers.ModelSerializer):
#     type = serializers.ChoiceField(
#         choices=TYPE_PROJECT,
#         style={'base_template':'radio.html'}
#     )

#     contributor = ContributorSerializer(many=True)
    
#     class Meta:
#         model = Project
#         fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'contributor']

#     def create(self, validated_data):
#         author = self.context['request'].user
#         project = Project.objects.create(
#             author_user_id=author,
#             **validated_data
#             )
#         return project