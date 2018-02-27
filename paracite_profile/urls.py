from django.urls import path

from paracite_profile import views

app_name = 'paracite_profile'

urlpatterns = [
    path('', views.index, name='index'),
]