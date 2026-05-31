# posts/comments 통합 참조 규칙을 검증하는 정적 회귀 테스트
from pathlib import Path
import unittest


BASE_DIR = Path(__file__).resolve().parent


def read_source(path):
    return (BASE_DIR / path).read_text(encoding='utf-8')


class PostsCommentsIntegrationStaticTests(unittest.TestCase):
    def test_posts_pages_are_wired_and_call_posts_api(self):
        config_source = read_source('config/urls.py')
        views_source = read_source('posts/views.py')
        list_template_path = BASE_DIR / 'posts/templates/posts/post_list.html'
        form_template_path = BASE_DIR / 'posts/templates/posts/post_form.html'

        self.assertIn('from posts import views as post_views', config_source)
        self.assertIn("path('posts/', post_views.post_list_page)", config_source)
        self.assertIn("path('posts/new/', post_views.post_create_page)", config_source)
        self.assertIn('def post_list_page(request):', views_source)
        self.assertIn("return render(request, 'posts/post_list.html')", views_source)
        self.assertIn('def post_create_page(request):', views_source)
        self.assertIn("return render(request, 'posts/post_form.html')", views_source)
        self.assertTrue(list_template_path.exists())
        self.assertTrue(form_template_path.exists())

        list_source = list_template_path.read_text(encoding='utf-8')
        form_source = form_template_path.read_text(encoding='utf-8')

        self.assertIn("fetch('/api/posts'", list_source)
        self.assertIn("href='/posts/new/'", list_source)
        self.assertIn("fetch('/api/posts'", form_source)
        self.assertIn("method: 'POST'", form_source)

    def test_posts_create_and_list_api_is_wired(self):
        config_source = read_source('config/urls.py')
        urls_source = read_source('posts/urls.py')
        views_source = read_source('posts/views.py')

        self.assertIn("include('posts.urls')", config_source)
        self.assertIn("PostListCreateView.as_view()", urls_source)
        self.assertIn('def get(self, request):', views_source)
        self.assertIn("Post.objects.select_related('author').order_by('-created_at')", views_source)
        self.assertIn('def post(self, request):', views_source)
        self.assertIn('serializer = PostSerializer(data=request.data)', views_source)
        self.assertIn('serializer.save(author=request.user)', views_source)
        self.assertIn('status=status.HTTP_201_CREATED', views_source)

    def test_my_posts_view_filters_by_author_field(self):
        source = read_source('users/views.py')

        self.assertIn('Post.objects.filter(author=request.user)', source)
        self.assertNotIn('Post.objects.filter(user=request.user)', source)

    def test_likes_imports_comment_from_comments_app(self):
        for path in ['likes/models.py', 'likes/views.py']:
            with self.subTest(path=path):
                source = read_source(path)

                self.assertIn('from posts.models import Post', source)
                self.assertIn('from comments.models import Comment', source)
                self.assertNotIn('from posts.models import Post, Comment', source)

    def test_likes_urls_use_single_api_prefix(self):
        config_source = read_source('config/urls.py')
        likes_source = read_source('likes/urls.py')

        self.assertIn("path('api/', include('likes.urls'))", config_source)
        self.assertIn("path('posts/<int:post_id>/likes'", likes_source)
        self.assertIn(
            "path('posts/<int:post_id>/comments/<int:comment_id>/likes'",
            likes_source,
        )
        self.assertNotIn("path('api/posts/", likes_source)


if __name__ == '__main__':
    unittest.main()
