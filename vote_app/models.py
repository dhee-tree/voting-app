from django.db import models


class UserVote(models.Model):
    email = models.EmailField(max_length=250)
    user_code = models.CharField(max_length=15)
    user_vote_count = models.IntegerField(default=0)


class Higher(models.Model):
    name = models.CharField(max_length=100)
    unit_one = models.CharField(max_length=100)
    unit_one_glh = models.IntegerField(default=0)

    unit_two = models.CharField(max_length=100)
    unit_two_glh = models.IntegerField(default=0)

    unit_three = models.CharField(max_length=100)
    unit_three_glh = models.IntegerField(default=0)

    points = models.IntegerField(default=0)

