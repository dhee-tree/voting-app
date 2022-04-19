from django.db import models


class Vote(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count


class UserVote(models.Model):
    email = models.EmailField(max_length=30)
    user_code = models.CharField(max_length=15)
    user_vote_count = models.IntegerField(default=0)
