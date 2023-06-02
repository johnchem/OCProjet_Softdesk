from rest_framework.permissions import BasePermission

from project.models import Project, Contributor
from authentification.models import User


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user 
                    and request.user.is_authenticated
                    and request.user.is_superuser
                    )
    
# class IsCollaborator(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         list_collaborator = 