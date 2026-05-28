# 댓글 API 요청과 응답 데이터를 변환하는 Serializer
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post_id',
            'content',
            'author_id',
            'author_nickname',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'post_id', 'author_id', 'author_nickname', 'created_at', 'updated_at']
