from django.db import models


class Users(models.Model):
    user_name = models.CharField(max_length=100)
    user_rank = models.IntegerField(default=0)

    def __str__(self):
        return self.user_name
