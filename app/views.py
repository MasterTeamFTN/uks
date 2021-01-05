from django.shortcuts import render
from app.models import Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    current_user = request.user
    context = {
        'projects': Project.objects.filter(contributors = current_user.id)
    }
    print (context)
    return render(request, 'app/home.html', context)

def about(request):
    return render(request, 'app/about.html')

def projects(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'app/projects.html', context);


class ProjectDetailView(DetailView):
    model = Project 

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project 
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user.id in project.contributors.all():
            return True
        return False


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project 
    fields = ['name', 'description', 'is_public', 'contributors']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
