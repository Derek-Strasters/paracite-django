from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from paracite_profile.models import Profile
from .models import Story, Paragraph


class IndexView(generic.ListView):
    template_name = 'cites/index.html'
    context_object_name = 'stories_previews'

    def get_queryset(self):
        return Story.objects.stories_previews()


def create_story(request):  # FIXME: Class based view???
    if request.method == 'POST':
        print()
    else:
        context = {
            'form': {
                'Title': {[
                    #  TODO: Fuck, this read the django docs for class based
                ]}
            }
        }
        return render(request, 'cites/story_form.html', context)


def detail_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    lead_paragraph = story.first_para()
    return render_detail(request, story, lead_paragraph)


def detail_para(request, paragraph_id):
    lead_paragraph = get_object_or_404(Paragraph, id=paragraph_id)
    story = Story.objects.get(id=lead_paragraph.story.id)
    return render_detail(request, story, lead_paragraph)


def detail_para_respond(request, paragraph_id):
    lead_paragraph = get_object_or_404(Paragraph, id=paragraph_id)
    story = Story.objects.get(id=lead_paragraph.story.id)
    return render_detail(request, story, lead_paragraph, is_response=True)


def render_detail(request, story, paragraph, is_response=False):
    filler = {'filler': 'No more alternative paragraphs'}
    paragraphs = [child.child_chain() for child in paragraph.children()]
    fillers = [filler] * max(4 - len(paragraphs), 0)
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

    return redirect(paragraph)
