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
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentification.views import UserViewSet
from project.views import ProjectViewset, AdminProjectViewset
from issues.views import IssuesViewset

router = routers.SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('projects', ProjectViewset, basename='projects')
router.register('admin/projects', AdminProjectViewset, basename='admin_projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register(r'issues', IssuesViewset, basename="issues")

issues_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
# issues_router.register(r'comments', CommentsViewset, basename='issues-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include(router.urls)),
    path('api/', include(project_router.urls)),
    path('api/', include(issues_router.urls)),
    ]

# urlpatterns += router.urls
