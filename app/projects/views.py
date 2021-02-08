from django.shortcuts import render
from .models import Project
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..tasks.models import Task

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

        if Project.objects.filter(name=form.instance.name).exists():
            form.add_error('name', 'This name already exists')
            return super().form_invalid(form)
        return super().form_valid(form)

def project_contributors(request, pk):
    project = Project.objects.get(pk=pk)

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
