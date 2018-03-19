from django.urls import path, register_converter

from . import converters, views

register_converter(converters.MakeURLWeird, 'shortened')

app_name = 'cites'

urlpatterns = [
    path('', views.index, name='index'),

    # Go to specific story
    path('s/<shortened:story_id>/', views.detail_story, name='detail_story'),

    # Go to paragraph in story
    path('p/<shortened:paragraph_id>', views.detail_para, name='detail_para'),

    # Go to specific paragraph in story, also used for POST operations
    path('p/<shortened:paragraph_id>/', views.post_para, name='post_para'),

    # Vote on a paragraph
    path('p/<shortened:paragraph_id>/vote/', views.vote, name='vote')
]
