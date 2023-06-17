from rest_framework import viewsets, status
from rest_framework.response import Response

from issues.models import Issues
from project.models import Contributor
from comments.models import Comments, CommentSerializer


# Create your views here.

class CommentsViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):

        issues_pk = self.kwargs.get("issues_pk", self.kwargs["pk"])
        return Comments.objects.filter(issues_id=issues_pk)

    def list(self, request, project_pk=None, pk=None):

        try:
            # check if the url is correct
            issue = Issues.objects.get(pk=pk)
            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_400_BAD_REQUEST
                )

            # check if the login user have right to access this endpoint
            contributors = Contributor.objects.filter(project_id__project_id=project_pk)
            if request.user not in [user.user_id for user in contributors]:
                return Response(
                    "vous n'êtes pas membre du projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return super().list(self, request, project_pk=None, pk=None)

        except Issues.DoesNotExist:
            return Response(
                "le problème n'existe pas",
                status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, project_pk=None, issues_pk=None, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
            issue = comment.issues_id

            # check if the url is correct
            if not comment.issues_id.issues_id == issues_pk:
                return Response(
                    "le commentaire n'appartient pas à ce problème",
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_400_BAD_REQUEST
                )

            # check if the login user have right to access this endpoint
            contributors = Contributor.objects.filter(project_id__project_id=project_pk)
            if request.user not in [user.user_id for user in contributors]:
                return Response(
                    "vous n'êtes pas membre du projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return super().retrieve(self, request, project_pk=None, pk=None)

        except Comments.DoesNotExist:
            return Response(
                "le commentaire n'existe pas",
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request, project_pk=None, pk=None):
        try:
            # check if the url is correct
            issue = Issues.objects.get(pk=pk)
            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_400_BAD_REQUEST
                )

            # check if the login user have right to access this endpoint
            contributors = Contributor.objects.filter(project_id__project_id=project_pk)
            if request.user not in [user.user_id for user in contributors]:
                return Response(
                    "vous n'êtes pas membre du projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            data = request.data.copy()
            data['issues_id'] = issue.issues_id
            data['author_user_id'] = request.user.user_id

            serializer = self.serializer_class(data=data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Issues.DoesNotExist:
            return Response(
                "le problème n'existe pas",
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, project_pk=None, issues_pk=None, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
            issue = comment.issues_id

            # check if the url is correct
            if not comment.issues_id.issues_id == issues_pk:
                return Response(
                    "le commentaire n'appartient pas à ce problème",
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_400_BAD_REQUEST
                )

            # check if the login user have right to access this endpoint
            if request.user != comment.author_user_id:
                return Response(
                    "vous n'êtes pas l'auteur du commentaire",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            serializer = self.serializer_class(
                comment,
                data=request.data,
                partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Comments.DoesNotExist:
            return Response(
                "le commentaire n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

    def delete(self, request, project_pk=None, issues_pk=None, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
            issue = comment.issues_id

            if not comment.issues_id.issues_id == issues_pk:
                return Response(
                    "le commentaire n'appartient pas à ce problème",
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_400_BAD_REQUEST
                )

            # check if the login user have right to access this endpoint
            if request.user != comment.author_user_id:
                return Response(
                    "vous n'êtes pas l'auteur du commentaire",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            comment.delete()
            return Response(
                "le commentaire est supprimé",
                status=status.HTTP_200_OK
                )

        except Comments.DoesNotExist:
            return Response(
                "le commentaire n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )
