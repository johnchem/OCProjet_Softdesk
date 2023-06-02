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
        return Issues.objects.all()
        
    def create(self, request, project_pk=None):
        data = request.data.copy()
        data['project_id']=Project.objects.get(pk=project_pk).project_id
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
        except issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IssuesSerializer(issue, data=request.data, partial=True)
        # setting raise_exception=True in the serializer's is_valid method will raise exception on error. So you don't have implement extra logics
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
    
    def delete(self, request, project_pk=None, pk=None):
        try:
            issue = Issues.objects.get(pk=pk)
            issue.delete()
            return Response(status=status.HTTP_200_OK)
        except issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(issue.errors, status=status.HTTP_204_NO_CONTENT)
 
 