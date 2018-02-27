from random import randrange

from django.db import models
from django.db.models import CASCADE, PROTECT

from paracite_profile.models import Profile
from .converters import id_to_url


# OMG, notes! OK this is to do stuff, so the authors can create their own
# stories and optionally only allow certain collaborators to participate, and
# can even control weather or not it is publicly visible or not.  A user can
# create their own private story or a few friends can craft a novel where the
# public can vote but not make edits (perhaps they can suggest edits)

# TODO: add validators to all relevant fields


class StoryManager(models.Manager):
    def create_story(self, author, title, text):
        story = self.create(author=author, title=title)
        url = id_to_url(story.id)
        self.update(url=url)

        paragraph = Paragraph(story=story, author=author, text=text, level=0)
        paragraph.save()

        return story


class ParagraphManager(models.Manager):
    def create_paragraph(self, author, parent_paragraph, text):
        level = parent_paragraph.level + 1
        score = randrange(5, 15)

        paragraph = self.create(story=parent_paragraph.story,
                                parent_paragraph=parent_paragraph,
                                author=author,
                                text=text,
                                score=score,
                                level=level)
        return paragraph


class VotingRecordManager(models.Manager):
    def create_vote(self, profile, paragraph, vote):
        self.create(profile=profile, paragraph=paragraph, vote=vote)


class Story(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('paracite_profile.Profile',
                               on_delete=PROTECT)

    score = models.BigIntegerField(default=0)
    url = models.URLField(max_length=8, unique=True)
    # FIXME: Should url be the PK?

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    objects = StoryManager()

    def __str__(self):
        return self.title


class Paragraph(models.Model):
    story = models.ForeignKey(Story, on_delete=CASCADE)
    parent_paragraph = models.ForeignKey('self',
                                         on_delete=CASCADE,
                                         blank=True,
                                         null=True)
    author = models.ForeignKey('paracite_profile.Profile',
                               on_delete=PROTECT,
                               related_name='author')
    text = models.CharField(max_length=4095)

    voters = models.ManyToManyField('paracite_profile.Profile',
                                    through='VotingRecord',
                                    related_name='voters')
    score = models.IntegerField()
    level = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    objects = ParagraphManager()

    def siblings(self):
        return self.story.paragraph_set.filter(
            parent_paragraph=self.parent_paragraph)

    def siblings_voted_by(self, profile):
        return self.story.paragraph_set.filter(
            parent_paragraph=self.parent_paragraph,
            votingrecord__profile=profile)

    def __str__(self):
        return self.text


class VotingRecord(models.Model):
    VERY_GOOD = 4
    GOOD = 3
    NEUTRAL = 2
    BAD = 1
    VERY_BAD = 0
    VOTE_CHOICES = (
        (VERY_GOOD, 'Very Good'),
        (GOOD, 'Good'),
        (NEUTRAL, 'Neutral'),
        (BAD, 'Bad'),
        (VERY_BAD, 'Very Bad'),
    )

    profile = models.ForeignKey('paracite_profile.Profile', on_delete=CASCADE)
    paragraph = models.ForeignKey(Paragraph, on_delete=CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    objects = VotingRecordManager()
