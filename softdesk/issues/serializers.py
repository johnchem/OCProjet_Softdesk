from rest_framework import serializers

from issues.models import Issues

class IssuesSerializer(serializers.ModelSerializer):
    project_id = serializers.SerializerMethodField(method_name="get_project_id")
    author_user_id = serializers.SerializerMethodField(method_name="get_author_user_id")
    assignee_user_id = serializers.SerializerMethodField(method_name="get_assignee_user_id")
    
    def get_project_id(self, obj):
        context_data = self.context.get('project_id', None)
        return context_data
    
    def get_author_user_id(self, obj):
        request_user = self.context.get('author_user_id')
        return request_user
    
    def get_assignee_user_id(self, obj):
        context_data = self.context.get('assignee_user_id', None)
        return context_data
    
    class Meta:
        model=Issues
        # fields=["title", "desc", "tag", "priority", "status"]
        fields = "__all__"