from django.urls import path

from comments.views import PostCommentListCreateView

from .views import PostDetailView, PostListCreateView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:post_id>', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comments', PostCommentListCreateView.as_view(), name='post-comment-list-create'),
]
