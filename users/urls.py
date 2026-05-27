from django.urls import path
from .views import SignupView, LoginView, LogoutView, MyPostsView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/posts/', MyPostsView.as_view()),
]