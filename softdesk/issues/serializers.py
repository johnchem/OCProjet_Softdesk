from rest_framework import serializers

from issues.models import Issues
from authentification.models import User
from project.models import Project

# from project.serializers import ProjectSerializer
from authentification.serializers import UserSerializer

# class IssuesSerializer(serializers.ModelSerializer):
#     # project_id=ProjectSerializer()
#     # assignee_user_id=UserSerializer()
#     # author_user_id=UserSerializer()

#     class Meta:
#         model=Issues
#         fields=(
#             "title", 
#             "desc", 
#             "tag", 
#             "priority", 
#             "status",
#             "project_id",
#             "author_user_id",
#             "assignee_user_id",
#         )

#     def create(self, validated_data):
#         issue = Issues.objects.create(
#             **validated_data,
#         )
#         return issue