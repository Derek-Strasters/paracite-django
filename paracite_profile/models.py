from django.db import models


class Profile(models.Model):
    user_name = models.CharField(unique=True, max_length=63)

    total_score = models.BigIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_name
