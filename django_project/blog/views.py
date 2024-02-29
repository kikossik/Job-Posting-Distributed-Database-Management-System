from django.shortcuts import render
from .models import Job


def home(request):
    context = {
        'jobs': Job.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
