from rest_framework import serializers

from comments.models import Comments

from issues.serializers import IssuesSerializer


class CommentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=(
            "comment_id",
            "author_user_id",
            "description",
            "created_time",
        )

    def __str__(self):
        return f"#{self.comment_id} - {self.author_user_id} : {self.description}"

class CommentsDetailSerializer(serializers.ModelSerializer):
    issues_id = IssuesSerializer()
    class Meta:
        model=Comments
        fields=(
            "comment_id",
            "description",
            "author_user_id",
            "issues_id",
            "created_time",
        )


    