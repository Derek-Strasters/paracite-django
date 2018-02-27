from django.urls import path, register_converter

from . import converters, views

register_converter(converters.MakeURLWeird, 'wwwwwwww')

app_name = 'cites'

urlpatterns = [
    path('', views.index, name='index'),
    path('<wwwwwwww:requested_story_id>/', views.detail, name='detail'),
]