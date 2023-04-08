from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.models import Group

from authentification.models import User
from authentification.serializers import UserSerializer, GroupSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    # @action(detail=True, methods=['get'])
    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

