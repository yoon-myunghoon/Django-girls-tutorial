from django.contrib.auth.models import User
from rest_framework import serializers
from blog.models import Post, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email', 'post_set']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'author', 'title', 'text', 'comments']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'author', 'text']