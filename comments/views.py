from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post

from .models import Comment
from .serializers import CommentSerializer


class PostCommentListCreateView(APIView):
    def get_post(self, post_id):
        return get_object_or_404(Post, id=post_id)

    def get(self, request, post_id):
        post = self.get_post(post_id)
        comments = post.comments.select_related('author').order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        post = self.get_post(post_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def get_object(self, comment_id):
        return get_object_or_404(Comment.objects.select_related('author', 'post'), id=comment_id)

    def patch(self, request, comment_id):
        comment = self.get_object(comment_id)

        if comment.author_id != request.user.id:
            return Response({'detail': '작성자만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)

        if comment.author_id != request.user.id:
            return Response({'detail': '작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
