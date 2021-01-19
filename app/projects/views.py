from django.shortcuts import render
from .models import Project, Branch, Commit
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..utils.github_utils import get_branches_and_commits

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
    fields = ['name', 'description', 'github_url', 'is_public', 'contributors']

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

def project_branches(request, pk):
    project = Project.objects.get(pk=pk)
    branches = Branch.objects.filter(project=project)

    context = {
        'project_id': project.pk,
        'project_name': project.name,
        'branches': branches
    }

    return render(request, 'app/project/branches.html', context=context)

def project_commits(request, pk):
    project = Project.objects.get(pk=pk)
    branch_name = request.GET.get('branch', '')
    branch = Branch.objects.get(name=branch_name, project=project)
    commits = Commit.objects.filter(branch=branch).all()

    context = {
        'project_id': project.pk,
        'project_name': project.name,
        'branch_name': branch_name,
        'commits': commits
    }

    return render(request, 'app/project/commits.html', context=context)

def project_refresh_branches(request, pk):
    project = Project.objects.get(pk=pk)

    Branch.objects.filter(project=project).delete()
    new_branches = get_branches_and_commits(project)

    context = {
        'project_id': project.pk,
        'project_name': project.name,
        'branches': new_branches
    }

    if new_branches is None:
        messages.warning(request, 'Github API error. Can\'t update branches')
    else:
        messages.success(request, 'Branches and commits were successfully updated')

    return render(request, 'app/project/branches.html', context=context)
