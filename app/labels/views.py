from django.shortcuts import render
from .models import Label
from ..projects.models import Project
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class LabelUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/label/label_form.html'
    model = Label
    fields = ['name', 'description', 'color']

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)

        if form.instance.name != self.get_object().name and Label.objects.filter(name=form.instance.name, project=project).exists():
            form.add_error('name', 'This name already exists')
            return super().form_invalid(form)

        form.instance.project = project
        return super().form_valid(form)

    def test_func(self):
        label = self.get_object()
        return self.request.user in label.project.contributors.all()

class LabelDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'app/label/label_confirm_delete.html'
    model = Label

    def get_success_url(self):
        label = self.get_object()
        return reverse_lazy('label-list', kwargs={'project_pk': label.project.id})

    def test_func(self):
        label = self.get_object()
        return self.request.user in label.project.contributors.all()

class LabelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app/label/label_form.html'
    model = Label
    fields = ['name', 'description', 'color']

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)

        if Label.objects.filter(name=form.instance.name, project=project).exists():
            form.add_error('name', 'This name already exists')
            return super().form_invalid(form)

        form.instance.project = project
        return super().form_valid(form)

    # TODO: iz nekog razloga ne zeli da prihvati ovu proveru
    # kad budes opet probavao ne zaboravi da dodas UserPassesTestMixin
    # u listu klasa za nasledjivanje
    def test_func(self):
        label = self.get_object()
        return self.request.user in label.project.contributors.all()

def label_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)

    context = {
        'labels': Label.objects.filter(project=project),
        'project': project
    }

    return render(request, 'app/label/label_list.html', context)
