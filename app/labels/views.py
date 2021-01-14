from django.shortcuts import render
from .models import Label
from ..projects.models import Project
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'app/label/label_form.html'
    model = Label
    fields = ['name', 'description', 'color']

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'app/label/label_confirm_delete.html'
    model = Label
    
    def get_success_url(self):
        label = self.get_object()
        return reverse_lazy('label-list', kwargs={'project_pk': label.project.id})

class LabelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app/label/label_form.html'
    model = Label
    fields = ['name', 'description', 'color']

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        form.instance.project = Project.objects.get(pk=project_id)
        return super().form_valid(form)

def label_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)

    context = {
        'labels': Label.objects.filter(project=project),
        'project': project
    }

    return render(request, 'app/label/label_list.html', context)