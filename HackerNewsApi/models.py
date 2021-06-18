from django.db import models
import uuid


class Posts(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    amount_of_upvotes = models.PositiveIntegerField(default=0)
    author_name = models.ForeignKey(
        'auth.User',
        related_name='posts',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'posts'
        ordering = ['creation_date']

class Comments(models.Model):
    author_name = models.ForeignKey(
        'auth.User',
        related_name='comment',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coments'
        ordering = ['creation_date']

class Votes(models.Model):
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    author_name = models.ForeignKey('auth.User', related_name='user_votes', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='post_votes', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)

    class Meta:
        db_table = 'votes'
        ordering = ['activity_type']


