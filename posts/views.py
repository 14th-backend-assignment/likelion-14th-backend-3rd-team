from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class PostListCreateView(APIView):
    def get(self, request):
        sort = request.query_params.get('sort', 'latest')

        if sort != 'latest':
            return Response(
                {'detail': '지원하지 않는 정렬 기준입니다.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        posts = Post.objects.select_related('author').order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get_object(self, post_id):
        return get_object_or_404(Post.objects.select_related('author'), id=post_id)

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, post_id):
        post = self.get_object(post_id)

        if post.author_id != request.user.id:
            return Response({'detail': '작성자만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = self.get_object(post_id)

        if post.author_id != request.user.id:
            return Response({'detail': '작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
