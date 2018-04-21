from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from paracite_profile.models import Profile
from .forms import NewStory, NewParagraph
from .models import Story, Paragraph


class IndexView(generic.ListView):
    template_name = 'cites/index.html'
    context_object_name = 'stories_previews'

    def get_queryset(self):
        return Story.objects.stories_previews()


def create_story(request):
    if request.method == "POST":
        form = NewStory(request.POST)

        if form.is_valid():
            story = Story.objects.create_story(Profile.objects.first(),
                                               form.cleaned_data['title'],
                                               form.cleaned_data['paragraph'])
            return redirect(story)
    else:
        form = NewStory()
        return render(request, 'cites/story_form.html', {'form': form})


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
    if request.method == "POST":
        form = NewParagraph(request.POST)
        if form.is_valid():
            new_para_text = form.cleaned_data['paragraph']
            Paragraph.objects.create_paragraph(Profile.objects.first(),
                                               new_para_text,
                                               paragraph)
        return redirect(paragraph)
    else:
        filler = {'filler': 'No more alternative paragraphs'}
        paragraphs = [child.child_chain() for child in paragraph.children()]
        fillers = [filler] * max(4 - len(paragraphs), 0)
        form = NewParagraph()
        context = {
            'story': story,
            'lead_paragraph': paragraph,
            'paragraphs': paragraphs,
            'fillers': fillers,
            'responding': is_response,
            'form': form,
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
