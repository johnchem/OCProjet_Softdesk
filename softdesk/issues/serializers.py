from rest_framework import serializers

from issues.models import Issues

class IssuesSerializer(serializers.ModelSerializer):
    project_id = serializers.SerializerMethodField()
    author_user_id = serializers.SerializerMethodField()
    assignee_user_id = serializers.SerializerMethodField()
    
    def get_project_id(self):
        context_data = self.context.get('project_id', None)
        return context_data
    
    def get_author_user_id(self):
        context_data = self.context.get('author_user_id', None)
        return context_data
    
    def get_assignee_user_id(self):
        context_data = self.context.get('assignee_user_id', None)
        return context_data
    
    class Meta:
        model=Issues
        # fields=["title", "desc", "tag", "priority", "status"]
        fields = "__all__"