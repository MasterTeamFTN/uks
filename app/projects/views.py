from django.shortcuts import render
from .models import Project
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def projects(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'app/project/projects.html', context)

class ProjectDetailView(DetailView):
    template_name = 'app/project/project_detail.html'
    model = Project 

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'app/project/project_confirm_delete.html'
    model = Project 
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user in project.contributors.all():
            return True
        return False

class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app/project/project_form.html'
    model = Project 
    fields = ['name', 'description', 'is_public', 'contributors']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def project_contributors(request, pk):
    project = Project.objects.get(pk=pk)

    context = { 
        'project_id': project.id,
        'project_name': project.name,
        'contributors': project.contributors.all()
    }

    return render(request, 'app/project/contributors.html', context=context)
