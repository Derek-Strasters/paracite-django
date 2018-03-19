from django.shortcuts import render

from .models import Profile


def index(request):
    #  TODO: create profile page, or sign-in/signup
    all_profiles = Profile.objects.all()
    context = {'all_profiles': all_profiles}
    return render(request, 'paracite_profile/index.html', context)
