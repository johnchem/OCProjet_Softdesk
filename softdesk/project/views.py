from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from project.models import Project, Contributor
from project.models import AUTHOR
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
        serializer = ProjectSerializer(
            data=request.data,
            context={'request': request}
            )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        project = serializer.save()
        print(request.user)
        contributor = ContributorSerializer(
            data={"user_id":request.user.user_id,
            "project_id":project.project_id,
            "role":AUTHOR}
            )
        
        if not contributor.is_valid():
            return Response(contributor.errors, status=status.HTTP_400_BAD_REQUEST)

        contributor.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        # setting raise_exception=True in the serializer's is_valid method will raise exception on error. So you don't have implement extra logics
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(project.errors, status=status.HTTP_204_NO_CONTENT)
    
class AdminProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()