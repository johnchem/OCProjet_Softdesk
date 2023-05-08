"""softdesk URL Configuration

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
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentification.views import UserViewSet
from project.views import ProjectViewset, AdminProjectViewset

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('projects', ProjectViewset, basename='projects')
router.register('admin/projects', AdminProjectViewset, basename='admin_projects')
router.register('projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include(router.urls)),
    # path('/signup/', ),
    # path('/projects/'),
    # path('/projects/{id}/'),
    # path('/projects/{id}/users/'),
    # path('/projects/{id}/users/{id}'),
    # path('/projects/{id}/issues/'),
    # path('/projects/{id}/issues/{id}'),
    # path('/projects/{id}/issues/{id}/comments/'),
    # path('/projects/{id}/issues/{id}/comments/{id}'),
]

# urlpatterns += router.urls
