from HackerNewsApi.models import Posts


def my_cron_job():
    Posts.objects.all().update(amount_of_upvotes = 10)
