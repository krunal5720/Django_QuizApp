import secrets

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    poll_result = models.BooleanField(default=False)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user_result = models.BooleanField(default=False)



    def __str__(self):
        return f'{self.user.username}-{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user_result}'

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()
    percentage = models.FloatField()


    def __str__(self):
        return f'{self.user.username} - {self.count} - {self.percentage}'
