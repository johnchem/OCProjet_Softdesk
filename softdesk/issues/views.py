from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issues
from project.models import Project
from authentification.models import User

from issues.serializers import IssuesSerializer

# Create your views here.
class IssuesViewset(viewsets.ModelViewSet):
    serializer_class = IssuesSerializer
    Permission_class = [IsAuthenticated]
    # form_class = IssuesForm

    def get_queryset(self):
        return Issues.objects.all()
        
    def create(self, request, project_pk):
        data = request.data.copy()
        data['project_id']=Project.objects.get(pk=project_pk).project_id
        data['author_user_id']=request.user.user_id
        data['assignee_user_id']=User.objects.get(
            first_name=request.POST.get('assignee')
            ).user_id

        print(data)
        serializer = IssuesSerializer(
            data=data,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)