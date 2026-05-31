from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout
from .serializers import SignupSerializer, LoginSerializer
from .models import User
from django.shortcuts import render

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# 회원가입
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "회원가입에 성공했습니다.",
                "email": user.email,
                "nickname": user.nickname,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                "status": "success",
                "message": "로그인에 성공했습니다.",
                "email": user.email,
                "nickname": user.nickname,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃
class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            "status": "success",
            "message": "로그아웃 되었습니다.",
        }, status=status.HTTP_200_OK)

# 내가 작성한 게시물
class MyPostsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from posts.models import Post
        posts = Post.objects.filter(author=request.user)
        data = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
            }
            for post in posts
        ]
        return Response({
            "status": "success",
            "message": "작성한 게시글을 불러왔습니다.",
            "data": data,
        }, status=status.HTTP_200_OK)
    
def signup_page(request):
    return render(request, 'users/signup.html')

def login_page(request):
    return render(request, 'users/login.html')

def myposts_page(request):
    return render(request, 'users/myposts.html')
