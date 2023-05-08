from rest_framework import serializers

from issues.models import Issues

class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Issues
        field=["title", "desc", "tag", "priority", "statut", "assignee_user_id"]