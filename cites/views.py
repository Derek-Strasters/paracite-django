from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Story, Paragraph


def index(request):
    stories_previews = Story.objects.stories_previews()
    context = {'stories_previews': stories_previews}
    return render(request, 'cites/index.html', context)


def detail_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    lead_paragraph = story.paragraph_set.get(level=0)  # TODO: try/catch
    return render_detail(request, story, lead_paragraph)


def detail_para(request, paragraph_id):
    lead_paragraph = get_object_or_404(Paragraph, id=paragraph_id)
    story = Story.objects.get(id=lead_paragraph.story.id)  # TODO: try/catch
    return render_detail(request, story, lead_paragraph)


def render_detail(request, story, paragraph):
    paragraphs = []
    fillers = []
    url_query = request.GET
    has_response = False

    print(url_query.get('is_response', default=False))
    if url_query.get('is_response', default=False) == 'true':
        has_response = True
    # TODO: is 'is_response' too hardcoded?

    for child in paragraph.children():
        paragraphs.append(child.child_chain())

    for _ in range(4 - len(paragraphs)):
        fillers.append({'filler': 'No more alternative paragraphs'})

    context = {
        'story': story,
        'lead_paragraph': paragraph,
        'paragraphs': paragraphs,
        'fillers': fillers,
        'responding': has_response,
    }
    return render(request, 'cites/detail.html', context)


def vote(request, paragraph_id):
    paragraph = get_object_or_404(Paragraph, id=paragraph_id)

    if request.method == "POST":
        vote_val = request.POST['v']  # TODO: add validation
        paragraph.score = paragraph.score + int(vote_val)
        paragraph.save()

        response = {'success': True}
    else:
        response = {'success': False,
                    'message': 'Bad request'}

    return JsonResponse(response)


def post_para(request, paragraph_id):
    paragraph = get_object_or_404(Paragraph, id=paragraph_id)

    if request.method == "POST":
        new_para_text = request.POST['new-para']
        print(new_para_text)
        # TODO: finish when profile is ready
        pass

    return detail_para(request, paragraph_id)
