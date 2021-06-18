import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from HackerNewsApi.models import Posts, Comments, Votes
from HackerNewsApi.permissions import IsOwnerOrReadOnly
from HackerNewsApi.serializers import (
    PostSerializer,
    UsersSerializer,
    CommentsSerializer,
)


class PostsList(generics.ListCreateAPIView):
    """Display all posts"""

    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author_name=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Display detail informations about post"""

    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentsList(generics.ListCreateAPIView):
    """Display all comments in post"""

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author_name=self.request.user)


class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Display detail informations about comment in post"""

    lookup_field = "id"
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserCreate(generics.CreateAPIView):
    """View for register a new user"""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.AllowAny]


class UserDetail(generics.RetrieveAPIView):
    """Display detail informations about user"""

    queryset = User.objects.all()
    serializer_class = UsersSerializer


class VotesView(APIView):
    """View for vote system"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, pk):
        body = json.loads(request.body)
        activity = body["activity_type"]
        post = Posts.objects.get(id=pk)
        user = User.objects.get(username=self.request.user)

        try:
            check_if_exist = Votes.objects.get(author_name_id=user.id, post_id=pk)
            if check_if_exist.activity_type == "U" and activity == "U":
                check_if_exist.activity_type = "D"
                check_if_exist.save()
                post.amount_of_upvotes += 1
                post.save()
            elif check_if_exist.activity_type == "D" and activity == "D":
                check_if_exist.activity_type = "U"
                check_if_exist.save()
                post.amount_of_upvotes -= 1
                post.save()
        except ObjectDoesNotExist:
            if activity == "U":
                Votes.objects.create(
                    author_name_id=user.id, post_id=pk, activity_type=activity
                )
                post.amount_of_upvotes += 1
                post.save()
            else:
                Votes.objects.create(
                    author_name_id=user.id, post_id=pk, activity_type=activity
                )
                post.amount_of_upvotes -= 1
                post.save()
        return Response(status=status.HTTP_200_OK)
