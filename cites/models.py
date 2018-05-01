from random import randrange

from django.db import models
from django.db.models import CASCADE, PROTECT
from django.urls import reverse

from paracite_profile.models import Profile
from .converters import id_to_url


# Notes (put in README): the authors can create their own
# stories and optionally allow only certain collaborators to participate, and
# can even control weather or not it is publicly visible or not.  A user can
# create their own private story or a few friends can craft a novel where the
# public can vote but not make edits (perhaps they can suggest edits)

# TODO: add validators to all relevant fields


class StoryManager(models.Manager):
    def create_story(self, author, title, text):
        story = self.create(author=author, title=title)
        Paragraph.objects.create_first_paragraph(story, author, text)

        return story

    def stories_previews(self, start=0, size=20):
        all_stories = self.all()[start:start + size]
        sp = [{'story': s, 'preview': s.first_para()} for s in all_stories]
        return sp


class ParagraphManager(models.Manager):
    def create_first_paragraph(self, story, author, text):
        level = 0
        score = randrange(5, 15)
        paragraph = self.create(story=story,
                                author=author,
                                text=text,
                                score=score,
                                level=level)
        return paragraph

    def create_paragraph(self, author, text, parent_paragraph):
        level = parent_paragraph.level + 1
        score = randrange(5, 15)
        paragraph = self.create(
            story=parent_paragraph.story,
            parent_paragraph=parent_paragraph,
            author=author,
            text=text,
            score=score,
            level=level)
        paragraph.save()

        return paragraph


class VotingRecordManager(models.Manager):
    def create_vote(self, profile, paragraph, vote):
        self.create(profile=profile, paragraph=paragraph, vote=vote)


class Story(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('paracite_profile.Profile',
                               on_delete=PROTECT)

    score = models.BigIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    # TODO: move the preceding to abstract base class or mixin
    objects = StoryManager()

    def get_absolute_url(self):
        return reverse('cites:detail_story', args=[id_to_url(self.id)])

    def first_para(self):
        return self.paragraph_set.get(level=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-score', 'created_date']


class Paragraph(models.Model):
    """Self referential object to accommodate a tree structure"""
    # Required
    story = models.ForeignKey(Story, on_delete=CASCADE)
    author = models.ForeignKey('paracite_profile.Profile',
                               on_delete=PROTECT,
                               related_name='author')
    text = models.TextField(max_length=4095)
    score = models.IntegerField()
    level = models.IntegerField()
    # Not required
    voters = models.ManyToManyField('paracite_profile.Profile',
                                    through='VotingRecord',
                                    through_fields=('paragraph', 'profile'),
                                    related_name='voters')
    parent_paragraph = models.ForeignKey('self',
                                         on_delete=CASCADE,
                                         blank=True,
                                         null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    objects = ParagraphManager()

    def get_absolute_url(self):
        return reverse('cites:detail_para', args=[id_to_url(self.id)])

    def get_vote_url(self):
        return reverse('cites:vote', args=[id_to_url(self.id)])

    def get_respond_url(self):
        return reverse('cites:detail_para_respond', args=[id_to_url(self.id)])

    def get_post_response_url(self):
        return reverse('cites:post_para', args=[id_to_url(self.id)])

    def children(self, start=0, size=4):
        """
        Returns the direct child paragraphs ordered by score
        :param start: specifies index to start from
        :param size: number of paragraphs to return
        :return:
        """
        return self.paragraph_set.exclude(id=self.id)[start:start + size]

    def siblings(self, start=0, size=3):
        """
        Returns a queryset of paragraphs that follow the same parent
        paragraph.
        :param size: number of paragraphs to return
        :param start: specifies index to start from
        :return: queryset of paragraphs
        """
        return self.parent_paragraph.paragraph_set.exclude(
            id=self.id)[start:start + size]

    def child_chain(self, max_count=20):
        """
        Returns a list starting with the original paragraph and up to 20 child
        paragraphs selected by the top score child from each level in order
        of level.
        :return: a list of paragraphs
        """
        paragraphs = []
        paragraph = self
        index = 0

        paragraphs.append(paragraph)

        while paragraph.paragraph_set.exists() and index < max_count:
            paragraph = paragraph.paragraph_set.first()
            paragraphs.append(paragraph)
            index += 1
        # TODO: This needs optimization to hit database less
        # TODO: USE https://github.com/django-mptt/django-mptt ?
        # TODO: OR send whole comment list and offload organization to js

        return paragraphs

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-score', 'created_date']


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

    profile = models.ForeignKey('paracite_profile.Profile',
                                on_delete=PROTECT)
    paragraph = models.ForeignKey(Paragraph, on_delete=PROTECT)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    objects = VotingRecordManager()
