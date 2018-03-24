from django.urls import path, register_converter

from . import converters, views

register_converter(converters.MakeURLWeird, 'shortened')

app_name = 'cites'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # Add new story
    path('s/create/', views.CreateStory.as_view(), name='new_story'),

    # Go to specific story
    path('s/<shortened:story_id>/', views.detail_story, name='detail_story'),

    # Go to paragraph in story
    path('p/<shortened:paragraph_id>/', views.detail_para, name='detail_para'),

    # Go to paragraph in story with response form open
    path('p/<shortened:paragraph_id>/respond/', views.detail_para_respond,
         name='detail_para_respond'),

    # Go to specific paragraph in story, also used for POST operations
    path('p/<shortened:paragraph_id>/post-para/', views.post_para,
         name='post_para'),

    # Vote on a paragraph
    path('p/<shortened:paragraph_id>/vote/', views.vote, name='vote')
]
