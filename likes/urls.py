from django.urls import path
from .views import PostLikeAPIView, CommentLikeAPIView

urlpatterns = [
    path('api/posts/<int:post_id>/likes', PostLikeAPIView.as_view()),
    path('api/posts/<int:post_id>/comments/<int:comment_id>/likes', CommentLikeAPIView.as_view()),
]

