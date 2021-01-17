from django.shortcuts import render
from .models import Task, Project, TaskVersion
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

class task_close_view(request, project_pk, pk):
    template_name = 'app/task/close_task.html'
    model = Task

    def get_success_url(self):
        task = self.get_object()
        return reverse_lazy('task-list', kwargs={'project_pk': task.project.id, 'task_pk': task.id})

    def test_func(self):
        task = self.get_object()
        return self.request.user in task.project.contributors.all()

def task_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    tasks = Task.objects.filter(project=project)
    context = {
        'tasks': tasks,
        'project': project,
    }

    return render(request, 'app/task/task_list.html', context)

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
