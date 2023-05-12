from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issues
from issues.serializers import IssuesSerializer
from project.models import Project
from authentification.models import User

# Create your views here.
class IssuesViewset(viewsets.ModelViewSet):
    serializer_class = IssuesSerializer
    Permission_class = [IsAuthenticated]

    def get_queryset(self):
        return Issues.objects.all()
    
    def create(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        print(request.POST)
        assignee = User.objects.get(first_name=request.POST.get('assignee'))
        print(str(assignee.user_id))

#
# probléme lors de la creation de l'Issues. la présence de l'assignee 
# n'est pas détecté par le validator
#

        serializer = IssuesSerializer(
            data=request.data,
            context={
                'author_user_id':request.user.user_id,
                'project_id':project.project_id,
                'assignee_user_id':assignee.user_id,
                },
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        issues=serializer.save()