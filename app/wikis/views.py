from django.shortcuts import render
from .models import Wiki, WikiVersion
from ..projects.models import Project
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def wikis_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)

    context = {
        'wikis': Wiki.objects.filter(project=project),
        'project': project
    }

    return render(request, 'app/wiki/wiki_list.html', context)

class WikiDetailView(DetailView):
    template_name = 'app/wiki/wiki_detail.html'
    model = Wiki

class WikiCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'app/wiki/wiki_form.html'
    model = Wiki
    fields = ['title', 'text']

    def form_valid(self, form):
        project_id = self.kwargs.get('project_pk')
        form.instance.project = Project.objects.get(pk=project_id)
        return super().form_valid(form)

    def test_func(self):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(pk=project_id)
        return self.request.user in project.contributors.all()

class WikiDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'app/wiki/wiki_confirm_delete.html'
    model = Wiki

    def get_success_url(self):
        wiki = self.get_object()
        return reverse_lazy('wiki-list', kwargs={'project_pk': wiki.project.id})

    def test_func(self):
        wiki = self.get_object()
        return self.request.user in wiki.project.contributors.all()

class WikiUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/wiki/wiki_form.html'
    model = Wiki
    fields = ['title', 'text']

    def test_func(self):
        wiki = self.get_object()
        return self.request.user in wiki.project.contributors.all()


def wiki_versions_list_view(request, project_pk, pk):
    wiki = Wiki.objects.get(pk=pk)

    context = {
        'wiki': wiki,
        'versions': WikiVersion.objects.filter(wiki=wiki).order_by('-updated_on')
    }

    return render(request, 'app/wiki/wikiversion_list.html', context)
