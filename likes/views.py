from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from posts.models import Post
from comments.models import Comment
from .models import PostLike, CommentLike

class PostLikeAPIView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "이미 좋아요를 눌렀습니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "게시글 좋아요 성공"}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = PostLike.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"detail": "게시글 좋아요 취소"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "좋아요를 누르지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

class CommentLikeAPIView(APIView):
    def post(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            return Response({"detail": "이미 좋아요를 눌렀습니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "댓글 좋아요 성공"}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
        like = CommentLike.objects.filter(user=request.user, comment=comment).first()
        if like:
            like.delete()
            return Response({"detail": "댓글 좋아요 취소"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "좋아요를 누르지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
