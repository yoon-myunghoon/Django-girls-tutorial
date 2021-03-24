from django.contrib.auth.models import User
from blog.models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework import permissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_date')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_date')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]