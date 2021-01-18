from django.shortcuts import render
from .models import Task, Project, TaskVersion, TaskState, Comment
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_currentuser.middleware import get_current_authenticated_user
from django.urls import reverse

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

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/task/task_form.html'
    model = Task
    fields = ['title', 'description', 'labels', 'assignees', 'milestone']

    def test_func(self):
        task = self.get_object()
        return self.request.user in task.assignees.all()

def task_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    tasks = Task.objects.filter(project=project)
    context = {
        'tasks': tasks,
        'project': project,
        'versions': TaskVersion.objects.all()
    }

    return render(request, 'app/task/task_list.html', context)

def board_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    tasks = Task.objects.filter(project=project)
    to_do = []
    in_progress = []
    review = []
    done = []
    for task in tasks:
        if task.current_state():
            if task.current_state().task_state == "TO_DO":
                to_do.append(task)
            if task.current_state().task_state  == "IN_PROGRESS":
                in_progress.append(task)
            if task.current_state().task_state == "REVIEW":
                review.append(task)
            if task.current_state().task_state == "DONE":
                done.append(task)

    context = {
        'to_do': to_do,
        'in_progress': in_progress,
        'review': review,
        'done': done,
        'project': project,
        'versions': TaskVersion.objects.all()
    }

    return render(request, 'app/task/board.html', context)

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

def progress_task(request, project_pk, pk):
    task = Task.objects.get(pk=pk)
    TaskVersion.objects.create(task=task, updated_by=get_current_authenticated_user(), task_state = TaskState.IN_PROGRESS)

    return board_view(request, project_pk)

def review_task(request, project_pk, pk):
    task = Task.objects.get(pk=pk)
    TaskVersion.objects.create(task=task, updated_by=get_current_authenticated_user(), task_state = TaskState.REVIEW)

    return board_view(request, project_pk)

def todo_task(request, project_pk, pk):
    task = Task.objects.get(pk=pk)
    TaskVersion.objects.create(task=task, updated_by=get_current_authenticated_user(), task_state = TaskState.TO_DO)

    return board_view(request, project_pk)

def done_task(request, project_pk, pk):
    task = Task.objects.get(pk=pk)
    TaskVersion.objects.create(task=task, updated_by=get_current_authenticated_user(), task_state = TaskState.DONE)

    return board_view(request, project_pk)

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
    comments = Comment.objects.filter(task=task).order_by('-updated_on')
    context = {
        'task': task,
        'comments': comments,
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

class CommentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'app/task/comment_form.html'
    model = Comment
    fields = ['text']
    def form_valid(self, form):
        task_id = self.kwargs.get('pk')
        form.instance.task = Task.objects.get(pk=task_id)
        return super().form_valid(form)

    def test_func(self):
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(pk=task_id)
        return self.request.user in task.project.contributors.all()
