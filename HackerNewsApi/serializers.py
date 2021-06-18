from rest_framework import serializers
from HackerNewsApi.models import Posts, Comments, Votes
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author_name.username')

    class Meta:
        model = Posts
        fields = ['id', 'title', 'link', 'creation_date', 'amount_of_upvotes', 'author_name']


class CommentsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author_name.username')

    class Meta:
        model = Comments
        fields = ['id', 'content', 'creation_date', 'author_name']


class UsersSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True, queryset=Posts.objects.all(), slug_field='title')
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'posts']

class VotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Votes
        fields=['activity_type']
