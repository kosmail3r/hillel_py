from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=280)
    brief_description = models.CharField(max_length=250)
    published_date = models.DateTimeField(null=True, auto_now_add=True)
    full_description = models.CharField(max_length=350)
    posted = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    username = models.CharField(max_length=250)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_com = models.BooleanField(default=False)

    def __str__(self):
        return self.text
