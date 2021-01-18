from django.shortcuts import render
from .models import Task, Project, TaskVersion, TaskState
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_currentuser.middleware import get_current_authenticated_user

class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'app/task/task_form.html'
    model = Task
    fields = ['title', 'description', 'labels', 'assignees', 'milestone']
    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        form.instance.project = Project.objects.get(pk=project_id)
        return super().form_valid(form)

    def test_func(self):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        return self.request.user in project.contributors.all()

def task_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    tasks = Task.objects.filter(project=project)
    context = {
        'tasks': tasks,
        'project': project,
        'versions': TaskVersion.objects.all()
    }

    return render(request, 'app/task/task_list.html', context)

def my_task_list_view(request):
    current_user = request.user
    tasks = Task.objects.filter(assignees=current_user.id)

    context = {
        'tasks': tasks
    }

    return render(request, 'app/task/user_task_list.html', context)

def close_task(request, project_pk, pk):
    task = Task.objects.get(pk=pk)
    TaskVersion.objects.create(task=task, updated_by=get_current_authenticated_user(), task_state = TaskState.DONE)

    context = {
        'task': task,
        'versions': TaskVersion.objects.filter(task=task).order_by('-updated_on')
    }

    return render(request, 'app/task/task_details.html', context)

def reopen_task(request, project_pk, pk):
    task = Task.objects.get(pk=pk)
    TaskVersion.objects.create(task=task, updated_by=get_current_authenticated_user(), task_state = TaskState.TO_DO)

    context = {
        'task': task,
        'versions': TaskVersion.objects.filter(task=task).order_by('-updated_on')
    }

    return render(request, 'app/task/task_details.html', context)

def task_detail_view(request, project_pk, pk):
    task = Task.objects.get(pk=pk)

    context = {
        'task': task,
        'versions': TaskVersion.objects.filter(task=task).order_by('-updated_on')
    }

    return render(request, 'app/task/task_details.html', context)

def task_contributors(request, pk):
    task = Task.objects.get(pk=pk)

    context = {
        'project_id': task.id,
        'project_name': project.name,
        'contributors': task.contributors.all()
    }

    return render(request, 'app/task/contributors.html', context=context)
