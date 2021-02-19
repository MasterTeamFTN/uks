from django.shortcuts import render
from .models import Milestone
from ..projects.models import Project
from ..tasks.models import Task
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render


class MilestoneCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'app/milestone/milestone_form.html'
    model = Milestone
    fields = ['title', 'description', 'due_date']

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        form.instance.project = Project.objects.get(pk=project_id)
        return super().form_valid(form)

    def test_func(self):
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_id)
        return self.request.user in project.contributors.all()

class MilestoneUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'app/milestone/milestone_form.html'
    model = Milestone
    fields = ['title', 'description', 'due_date']
    def get_success_url(self):
        milestone = self.get_object()
        return reverse_lazy('milestone-list', kwargs={'project_pk': milestone.project.id})
    def test_func(self):
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_id)
        return self.request.user in project.contributors.all()

class MilestoneDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'app/milestone/milestone_confirm_delete.html'
    model = Milestone

    def get_success_url(self):
        milestone = self.get_object()
        return reverse_lazy('milestone-list', kwargs={'project_pk': milestone.project.id})
    def test_func(self):
        milestone = self.get_object()
        return self.request.user in milestone.project.contributors.all()

def milestone_detail_view(request, project_pk, pk):
    milestone = Milestone.objects.get(pk=pk)
    tasks = Task.objects.filter(milestone=milestone)
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
        'object': milestone,
        'open_tasks': open_tasks,
        'closed_tasks': closed_tasks,
        'percent_done': percentage
    }
    return render(request, 'app/milestone/milestone_detail.html', context)

def milestone_list_view(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    context = {
        'milestones': Milestone.objects.filter(project=project),
        'project': project
    }
    return render(request, 'app/milestone/milestone_list.html', context)
