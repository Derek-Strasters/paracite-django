from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from paracite_profile.models import Profile
from .converters import id_to_url
from .models import Story, Paragraph


class IndexView(generic.ListView):
    template_name = 'cites/index.html'

    def get_queryset(self):
        return


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


def detail_para_respond(request, paragraph_id):
    lead_paragraph = get_object_or_404(Paragraph, id=paragraph_id)
    story = Story.objects.get(id=lead_paragraph.story.id)  # TODO: try/catch
    return render_detail(request, story, lead_paragraph, is_response=True)


def render_detail(request, story, paragraph, is_response=False):
    paragraphs = []
    fillers = []

    for child in paragraph.children():
        paragraphs.append(child.child_chain())

    for _ in range(4 - len(paragraphs)):
        fillers.append({'filler': 'No more alternative paragraphs'})

    context = {
        'story': story,
        'lead_paragraph': paragraph,
        'paragraphs': paragraphs,
        'fillers': fillers,
        'responding': is_response,
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
        # TODO: add data validation
        Paragraph.objects.create_paragraph(Profile.objects.first(),
                                           new_para_text,
                                           paragraph)
        # TODO: finish when profile is ready
        pass

    return redirect('cites:detail_para', paragraph_id=id_to_url(paragraph_id))
