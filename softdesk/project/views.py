from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from project.models import Project, Contributor
from project.serializers import (
    ProjectSerializer,
    ContributorSerializer
)

# Create your views here.
class ProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()
    
    def create(self, request):
        author = request.user
        serializer = ProjectSerializer(data=request.data)
        serializer.author_user_id = author
        if serializer.is_valid():
            return Response({'status': 'project saved'})
    
class AdminProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()