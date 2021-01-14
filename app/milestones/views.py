from django.shortcuts import render
from .models import Milestone
from ..projects.models import Project
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        project = Project.objects.get(pk=project_id)
        return self.request.user in project.contributors.all()

class MilestoneUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'app/milestone/milestone_form.html'
    model = Milestone
    fields = ['title', 'description', 'due_date']
    def get_success_url(self):
        milestone = self.get_object()
        return reverse_lazy('milestone-list', kwargs={'project_pk': milestone.project.id})

class MilestoneDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'app/milestone/milestone_confirm_delete.html'
    model = Milestone

    def get_success_url(self):
        milestone = self.get_object()
        return reverse_lazy('milestone-list', kwargs={'project_pk': milestone.project.id})

class MilestoneDetailView(DetailView):
    template_name = 'app/milestone/milestone_detail.html'
    model = Milestone

def milestone_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)

    context = {
        'milestones': Milestone.objects.filter(project=project),
        'project': project
    }

    return render(request, 'app/milestone/milestone_list.html', context)
