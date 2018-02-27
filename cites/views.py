from django.shortcuts import render, get_object_or_404

from .models import Story


def index(request):
    all_stories = Story.objects.all()
    context = {'all_stories': all_stories}
    return render(request, 'cites/index.html', context)


def detail(request, requested_story_id):
    story = get_object_or_404(Story, id=requested_story_id)

    paragraphs = [[]]
    for paragraph in story.paragraph_set.all().order_by('level',
                                                        'score',
                                                        'created_date'):
        if paragraph.level + 1 == len(paragraphs):
            paragraphs[paragraph.level].append(paragraph)
        else:
            paragraphs.append([paragraph])

    context = {
        'story': story,
        'paragraphs': paragraphs
    }
    return render(request, 'cites/detail.html', context)
