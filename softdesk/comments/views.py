from rest_framework import viewsets, status
from rest_framework.response import Response

from issues.models import Issues
from authentification.models import User
from comments.models import Comments

from comments.serializers import CommentsSerializer

# Create your views here.

class CommentsViewset(viewsets.ModelViewSet):
    serializer_class=CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()
    
    def create(self, request, project_pk=None, issue_pk=None):
        data = request.data.copy()
        data['issues_id']=Issues.objects.get(pk=issue_pk).issues_id
        data['author_user_id']=request.user.user_id

        serializer=CommentsSerializer(
            data=data
        )

        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, project_pk=None, issue_pk=None, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
        except comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentsSerializer(comment, data=request.data, partial=True)
        # setting raise_exception=True in the serializer's is_valid method will raise exception on error. So you don't have implement extra logics
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
    
    def delete(self, request, project_pk=None, issue_pk=None, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
            comment.delete()
            return Response(status=status.HTTP_200_OK)
        except comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(comment.errors, status=status.HTTP_204_NO_CONTENT)
 