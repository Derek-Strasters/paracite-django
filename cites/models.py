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

    def stories_previews(self, start=0, size=20):
        all_stories = self.all()[start:start + size]
        stories_previews = []
        for story in all_stories:
            original_paragraph = story.paragraph_set.get(level=0)
            stories_previews.append({'story': story,
                                     'preview': original_paragraph})
        return stories_previews

    def update_urls(self):
        all_stories = self.only('url', 'id').select_for_update().all()
        for story in all_stories:
            story.url = id_to_url(story.id)
            story.save()


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

    def update_urls(self):
        all_paragraphs = self.only('url', 'id').select_for_update().all()
        for paragraph in all_paragraphs:
            paragraph.url = id_to_url(paragraph.id)
            paragraph.save()


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
    # TODO: move the preceding to abstract base class
    objects = StoryManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-score', 'created_date']


class Paragraph(models.Model):
    """Self referential object to accommodate a tree structure"""
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
                                    through_fields=(
                                        'paragraph', 'profile'),
                                    related_name='voters')
    score = models.IntegerField()
    url = models.URLField(max_length=8, unique=True)
    level = models.IntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    objects = ParagraphManager()

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

        queryset = self.paragraph_set.all()
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
