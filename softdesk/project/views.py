from django.shortcuts import render
from rest_framework import viewsets
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

    def get_queryset(self):
        return Project.objects.all()
    
class AdminProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()