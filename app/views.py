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

# Error handlers
def error_400(request, exception):
    return render(request, '400.html')

def error_403(request, exception):
    return render(request, '403.html')

def error_404(request, exception):
    return render(request, '404.html')

def error_500(request, *args, **argv):
    return render(request, '500.html')
