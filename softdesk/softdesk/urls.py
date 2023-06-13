"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

from authentification.views import UserViewset
from project.views import ProjectViewset, ProjectUserViewset
from issues.views import IssuesViewset
from comments.views import CommentsViewset

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="obtain_tokens"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("users/", UserViewset.as_view({"get": "list"})),
    path("signup/", UserViewset.as_view({"post": "create_new_user"})),
    path(
        "projects/",
        ProjectViewset.as_view(
            {
                "post": "create",
                "get": "list",
            }
        ),
    ),
    path(
        "projects/<int:pk>/",
        ProjectViewset.as_view(
            {
                "put": "update",
                "delete": "delete",
                "get": "retrieve",
            }
        ),
    ),
    path(
        "projects/<int:pk>/users/",
        ProjectUserViewset.as_view(
            {
                "post": "add_collaborator",
                "get": "list_collaborator",
            }
        ),
    ),
    path(
        "projects/<int:project_pk>/users/<int:pk>",
        ProjectUserViewset.as_view(
            {
                "delete": "remove_user",
            }
        ),
    ),
    path(
        "projects/<int:pk>/issues/",
        IssuesViewset.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "projects/<int:project_pk>/issues/<int:pk>",
        IssuesViewset.as_view(
            {
                "put": "update",
                "delete": "delete",
            }
        ),
    ),
    path(
        "projects/<int:project_pk>/issues/<int:pk>/comments/",
        CommentsViewset.as_view(
            {
                "post": "create",
                "get": "list",
            }
        ),
    ),
    path(
        "projects/<int:project_pk>/issues/<int:issues_pk>/comments/<int:pk>",
        CommentsViewset.as_view(
            {
                "put": "update",
                "delete": "delete",
                "get": "retrieve",
            }
        ),
    ),
]
