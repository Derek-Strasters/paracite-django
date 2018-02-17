from django.db import models

from paracite_profile.models import Profile


# Holds primary key
class Story(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    score = models.BigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    rank = models.IntegerField()

    def __str__(self):
        return self.title


class Paragraph(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    parent_paragraph = models.ForeignKey('self', on_delete=models.CASCADE,
                                         blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    paragraph_text = models.CharField(max_length=4095)
    level = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.paragraph_text
