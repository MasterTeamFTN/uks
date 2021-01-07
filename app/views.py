from django.shortcuts import render
from app.models import Project

def home(request):
    current_user = request.user
    context = {
        'projects': Project.objects.filter(contributors = current_user.id)
    }
    print (context)
    return render(request, 'app/home.html', context)

def about(request):
    return render(request, 'app/about.html')
