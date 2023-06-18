
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.models import Project, Contributor
from project.models import ProjectSerializer, ContributorSerializer
from project.models import AUTHOR, CONTRIBUTOR

from authentification.models import User


# Create your views here.
class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributor__user_id=user)

    def create(self, request):
        serializer = ProjectSerializer(
            data=request.data,
            context={'request': request}
            )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        # save the project and create a contributor entry for the author
        project = serializer.save()
        contributor = ContributorSerializer(
            data={
                "user_id": request.user.user_id,
                "project_id": project.project_id,
                "role": AUTHOR}
            )

        if not contributor.is_valid():
            return Response(
                contributor.errors,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        contributor.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )

    def update(self, request, pk):
        try:
            # check the right to access the function
            project = Project.objects.get(project_id=pk)
            if request.user.user_id is not project.author_user_id.user_id:
                return Response(
                    "Fonction accessible à l'auteur du projet uniquement",
                    status=status.HTTP_403_FORBIDDEN
                    )

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

        serializer = ProjectSerializer(
            project,
            data=request.data,
            partial=True
            )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

        serializer.save(user=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )

    def delete(self, request, pk):
        try:
            # check the right to access the function
            project = Project.objects.get(project_id=pk)
            if request.user.user_id is not project.author_user_id.user_id:
                return Response(
                    "Fonction accessible à l'auteur du projet uniquement",
                    status=status.HTTP_403_FORBIDDEN
                    )

            project.delete()
            return Response(
                "Le projets et ses problèmes ont bien été supprimés",
                status=status.HTTP_200_OK
                )

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

        except:
            return Response(
                project.errors,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    def retrieve(self, request, pk=None):
        try:
            # check the right to access the function
            project = Project.objects.get(project_id=pk)
            contributor = Contributor.objects.filter(
                project_id=pk
                ).filter(
                role=[AUTHOR, CONTRIBUTOR]
                )
            if request.user not in contributor:
                return Response(
                    "Fonction accessible aux contributeurs du projet uniquement",
                    status=status.HTTP_403_FORBIDDEN,
                    )

            serializer = ProjectSerializer(project)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )


class ProjectUserViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def add_collaborator(self, request, pk=None):
        try:
            # check the right to access the function
            project = Project.objects.get(pk=pk)
            if not project.author_user_id.user_id == request.user.user_id:
                return Response(
                    "Fonction accessible à l'auteur du projet uniquement",
                    status=status.HTTP_403_FORBIDDEN,
                )

            # gaather the data to create the new contributor
            user = User.objects.get(
                    email=request.POST.get('email')
                )
            project = Project.objects.get(pk=pk)
            role = "C"

            contributor = Contributor.objects.create(
                user_id=user,
                project_id=project,
                role=role,
            )
            contributor.save()
            return Response(
                "Utilisateur ajouté",
                status=status.HTTP_201_CREATED
                )

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

        except User.DoesNotExist:
            return Response(
                "l'utilisateur n'est pas enregistré",
                status=status.HTTP_404_NOT_FOUND
                )

    def list_collaborator(self, request, pk):
        # check the right to access the function
        collaborators = User.objects.filter(member_of__project_id=pk)
        if request.user not in [user for user in collaborators]:
            return Response(
                "Fonction accessible aux contributeurs du projet uniquement",
                status=status.HTTP_403_FORBIDDEN,
                )
        try:
            project = Project.objects.get(pk=pk)
            collaborators = Contributor.objects.filter(project_id=project.project_id)
            serializer = ContributorSerializer(collaborators, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
                )

        except Project.DoesNotExist:
            return Response(
                "le project n'existe pas",
                status=status.HTTP_404_NOT_FOUND
                )

    def remove_user(self, request, project_pk, pk):
        try:
            # check the right to access the function
            project = Project.objects.get(pk=project_pk)
            if not project.author_user_id.user_id == request.user.user_id:
                return Response(
                    "Fonction accessible à l'auteur du projet uniquement",
                    status=status.HTTP_403_FORBIDDEN,
                )

            collaborator = Contributor.objects.filter(
                project_id=project_pk
            ).filter(
                user_id=pk
            )
            collaborator.delete()
            return Response(
                "Collabarateur retiré du projet",
                status=status.HTTP_200_OK
                )

        except Contributor.DoesNotExist:
            return Response(
                "l'utilisateur ne collabore pas au projet",
                status=status.HTTP_400_BAD_REQUEST
                )
