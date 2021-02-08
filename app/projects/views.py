from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Project, Branch, Commit
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..tasks.models import Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from ..utils.github_utils import get_branches_and_commits


class ProjectsListView(ListView):
    model = Project
    template_name = 'app/project/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query is None:
            return Project.objects.all()

        return Project.objects.filter(name__icontains=query)

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
    fields = ['name', 'description', 'github_url', 'is_public']

    def form_valid(self, form):
        form.instance.author = self.request.user

        if Project.objects.filter(name=form.instance.name).exists():
            form.add_error('name', 'This name already exists')
            return super().form_invalid(form)
        
        return super().form_valid(form)

def project_contributors(request, pk):
    project = get_object_or_404(Project, pk=pk)

    context = {
        'project_id': project.id,
        'project_name': project.name,
        'contributors': project.contributors.all()
    }

    return render(request, 'app/project/contributors.html', context=context)

def project_pulse(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = Task.objects.filter(project=project)
    open_tasks = []
    closed_tasks = []
    for task in tasks:
        if task.current_state():
            if task.current_state().task_state == "DONE":
                closed_tasks.append(task)
            else:
                open_tasks.append(task)
    percentage = 0
    if len(open_tasks) + len(closed_tasks) != 0:
        percentage =  round(len(closed_tasks)/(len(open_tasks) + len(closed_tasks)) * 100)

    context = {
        'object': project,
        'open_tasks': open_tasks,
        'closed_tasks': closed_tasks,
        'percent_done': percentage
    }
    return render(request, 'app/project/statistics_pulse.html', context)
def project_branches(request, pk):
    project = get_object_or_404(Project, pk=pk)
    branches = Branch.objects.filter(project=project)

    context = {
        'project_id': project.pk,
        'project_name': project.name,
        'branches': branches
    }

    return render(request, 'app/project/branches.html', context=context)

def project_commits(request, pk):
    project = get_object_or_404(Project, pk=pk)
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
    project = get_object_or_404(Project, pk=pk)

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

@login_required
def add_member(request, pk):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    project = get_object_or_404(Project, pk=pk)

    if request.user not in project.contributors.all():
        return HttpResponseForbidden('403 forbidden')

    username = request.POST['member_username']

    try:
        user = User.objects.get(username=username)
    except:
        messages.warning(request, f'Error! User {username} doesn\'t exist.')
        return redirect('project-contributors', pk)

    if user in project.contributors.all():
        messages.warning(request, f'User {username} is already in the members list.')
        return redirect('project-contributors', pk)

    project.contributors.add(user)

    messages.success(request, f'User {username} has been added to the project.')
    return redirect('project-contributors', pk)

@login_required
def delete_member(request, pk, member_id):
    project = get_object_or_404(Project, pk=pk)

    if request.user not in project.contributors.all():
        return HttpResponseForbidden('403 forbidden')

    try:
        user = User.objects.get(pk=member_id)
    except:
        messages.warning(request, f'Error! User doesn\'t exist.')
        return redirect('project-contributors', pk)

    if request.user == user:
        messages.warning(request, f'Error! You can\'t delete yourself.')
        return redirect('project-contributors', pk)

    username = user.username
    project.contributors.remove(user)

    messages.success(request, f'User {username} has been removed from the project.')
    return redirect('project-contributors', pk)

def project_settings(request, pk):
    project = get_object_or_404(Project, pk=pk)

    context = {
        'project': project
    }

    return render(request, 'app/project/settings.html', context=context)

class ProjectEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/project/project_edit.html'
    model = Project
    fields = ['name', 'description', 'is_public']

    def form_valid(self, form):
        form.instance.author = self.request.user

        if Project.objects.filter(name=form.instance.name).exists():
            if self.get_object().name != form.instance.name:
                form.add_error('name', 'This name already exists')
                return super().form_invalid(form)
        
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        return self.request.user in project.contributors.all()
