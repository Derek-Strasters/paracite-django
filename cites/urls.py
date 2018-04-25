from django.urls import path, register_converter

from . import converters, views

register_converter(converters.MakeURLSmall, 'shortened')

app_name = 'cites'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # Add new story
    path('s/create/', views.create_story, name='new_story'),

    # Go to specific story
    path('s/<shortened:story_id>/', views.detail_story, name='detail_story'),

    # Go to paragraph in story
    path('p/<shortened:paragraph_id>/', views.detail_para, name='detail_para'),

    # Go to paragraph in story with response form open
    path('p/<shortened:paragraph_id>/respond/', views.detail_para_respond,
         name='detail_para_respond'),

    # Vote on a paragraph
    path('p/<shortened:paragraph_id>/vote/', views.vote, name='vote'),

    # Register new user
    path('register/', views.UserFormView.as_view(), name='register')
]
