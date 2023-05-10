from rest_framework import serializers

from issues.models import Issues

class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Issues
        fields=["title", "desc", "tag", "priority", "status"]