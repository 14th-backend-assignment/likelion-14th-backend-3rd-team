# 게시글 API 요청과 응답 데이터를 변환하는 Serializer
from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author_id',
            'author_nickname',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'author_id', 'author_nickname', 'created_at', 'updated_at']
