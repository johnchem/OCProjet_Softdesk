from .models import User
from django.contrib.auth.models import Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        Model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']