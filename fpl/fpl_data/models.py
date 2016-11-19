from django.db import models


class Users(models.Model):
    user_name = models.CharField(max_length=100)
    user_rank = models.IntegerField(default=0)
    user_total = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

    def __str__(self):
        # return '%s', '%s', '%s' % (self.user_name, str(self.user_rank), str(self.user_total))
        return self.user_name    # + " - " + str(self.user_total)

    # def __str__(self):
    #    return str(self.user_total)


class Players(models.Model):
    player_name = models.CharField(max_length=100)

    def __str__(self):
        return self.player_name
