from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issues, IssuesSerializer
from project.models import Project
from authentification.models import User


# Create your views here.
class IssuesViewset(viewsets.ModelViewSet):
    serializer_class = IssuesSerializer
    Permission_class = [IsAuthenticated]
    # form_class = IssuesForm

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Issues.objects.filter(project_id=pk)
        
    def create(self, request, pk=None):
        data = request.data.copy()
        data['project_id']=Project.objects.get(pk=pk).project_id
        data['author_user_id']=request.user.user_id
        data['assignee_user_id']=User.objects.get(
            first_name=request.POST.get('assignee')
            ).user_id
        serializer = IssuesSerializer(
            data=data,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, project_pk=None, pk=None):
        try:
            issue = Issues.objects.get(pk=pk)
            
            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_401_UNAUTHORIZED
                )

            serializer = IssuesSerializer(issue, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data)
        
        except issue.DoesNotExist:
            return Response(
                "le problème n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

    def delete(self, request, project_pk=None, pk=None):
        try:
            issue = Issues.objects.get(pk=pk)

            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            issue.delete()
            return Response(
                "Le problème à bien été supprimé",
                status=status.HTTP_200_OK,
                )
        except issue.DoesNotExist:
            return Response(
                "Le problème n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(issue.errors, status=status.HTTP_204_NO_CONTENT)