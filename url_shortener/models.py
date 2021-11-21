from django.contrib.auth import get_user_model
from django.db import models


class Url(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    original = models.CharField(max_length=250)
    shortcut = models.CharField(max_length=280)
    redirect_count = models.IntegerField()

    def __str__(self):
        return self.shortcut

    def increaseRedirection(self):
        self.redirect_count += 1
        self.save()
