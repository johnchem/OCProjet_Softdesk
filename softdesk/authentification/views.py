from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from authentification.models import User
from authentification.serializers import (
    UserSerializer,
    SignUpSerializer
    )
# Create your views here.


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=["post"], url_path="signup", url_name='signup')
    def create_new_user(self, request, pk=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="users", url_name="users")
    def list_users(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
