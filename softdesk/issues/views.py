from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from issues.models import Issues, IssuesSerializer
from project.models import Project, Contributor
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
        try:
            # access granted only to contributor
            project = Project.objects.get(pk=pk)
            contributor = [user.user_id for user in Contributor.objects.filter(project_id=project)]
            if request.user not in contributor:
                return Response(
                    "vous n'êtes pas membre de ce projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # copy and update data with user_id instead of user instance
            data = request.data.copy()
            data['project_id'] = Project.objects.get(pk=pk).project_id
            data['author_user_id'] = request.user.user_id

            # get assignee name or author by defaut
            assignee_name = request.POST.get('assignee', request.user.first_name)
            assignee = User.objects.get(
                first_name=assignee_name
                )

            # the assignee and reject request if he's not contributor
            if assignee not in contributor:
                return Response(
                    "le responsable de la tâche doit être membre de ce projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            data['assignee_user_id'] = assignee.user_id

            # creation of the issue
            serializer = IssuesSerializer(
                data=data,
            )

            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                    )

            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

    def list(self, request, pk=None):
        try:
            # check if the login user have right to access this endpoint
            project = Project.objects.get(pk=pk)
            contributor = Contributor.objects.filter(project_id=project)
            if request.user not in [user.user_id for user in contributor]:
                return Response(
                    "vous n'êtes pas membre de ce projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            # return list function of the inherited
            return super().list(self, request, pk=None)

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

    def update(self, request, project_pk=None, pk=None):
        try:
            # check if the url is correct
            issue = Issues.objects.get(pk=pk)
            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # check if the login user have right to access this endpoint
            project = Project.objects.get(pk=project_pk)
            issue_author = issue.author_user_id
            if request.user != issue_author:
                return Response(
                    "vous n'êtes pas l'auteur du projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # creation of the mutable copy of the request.data
            data = request.data.copy()

            # check if the assignee is contributor
            if "assignee" in request.POST:
                contributors = Contributor.objects.filter(project_id=project)
                assignee = User.objects.get(
                    first_name=request.POST.get('assignee')
                    )

                if assignee not in [user.user_id for user in contributors]:
                    return Response(
                        "le responsable de la tâche doit être membre de ce projet",
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

                data['assignee_user_id'] = assignee.user_id

            # update of the issue
            serializer = IssuesSerializer(issue, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data)

        except Issues.DoesNotExist:
            return Response(
                "le problème n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

    def delete(self, request, project_pk=None, pk=None):
        try:
            # check if the url is correct
            issue = Issues.objects.get(pk=pk)
            if not issue.project_id.project_id == project_pk:
                return Response(
                    "le problème n'appartient pas à ce projet",
                    status=status.HTTP_400_BAD_REQUEST
                )

            # check if the login user have right to access this endpoint
            issue_author = issue.author_user_id
            if request.user != issue_author:
                return Response(
                    "vous n'êtes pas l'auteur du projet",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            issue.delete()
            return Response(
                "Le problème à bien été supprimé",
                status=status.HTTP_200_OK,
            )

        except Issues.DoesNotExist:
            return Response(
                "Le problème n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )
