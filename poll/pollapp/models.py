from django.db import models
from django.contrib.auth import get_user_model


class Question(models.Model):
    text = models.TextField(max_length=255, blank=False, null=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField(max_length=255, blank=False, null=False)
    question = models.ForeignKey(
        Question,
        related_name="answers",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    votes = models.ManyToManyField(
        get_user_model(),
        related_name="votes",
        through="vote",
        through_fields=("answer", "user"),
    )

    def __str__(self):
        return "(" + str(self.question) + ") " + self.text


class Vote(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user"
    )
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="vote")
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "answer"),)
