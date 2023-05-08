from rest_framework import viewset, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issues
from issues.serializers import IssuesSerializer
from project.models import Project
from authentification.models import User

# Create your views here.
class IssuesViewset(viewset.ModelViewSet):
    serializer_class = IssuesSerializer
    Permission_class = [IsAuthenticated]

    def get_queryset(self):
        return Issues.objects.all()
    
    def create(self, request, pk):
        project = Project.objects.get(pk=pk)
        assignee = User.object.get(first_name=request.POST["assignee"])

        serializer = IssuesSerializer(
            data=request.data,
            context={
                'request':request,
                'project_id':project["project_id"],
                'assignee_user_id':assignee["user_id"],
                },
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        issues=serializer.save()