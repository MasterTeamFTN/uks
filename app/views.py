from django.shortcuts import render
from app.models import Label, Project, Wiki, WikiVersion
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    current_user = request.user
    context = {
        'projects': Project.objects.filter(contributors = current_user.id)
    }
    print (context)
    return render(request, 'app/home.html', context)

def about(request):
    return render(request, 'app/about.html')

def projects(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'app/projects.html', context);

def labels(request):
    context = {
        'labels': Label.objects.all()
    }
    return render(request, 'app/labels.html', context)

class ProjectDetailView(DetailView):
    model = Project 

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project 
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user in project.contributors.all():
            return True
        return False


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project 
    fields = ['name', 'description', 'is_public', 'contributors']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name', 'description', 'color']

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    success_url = '/labels'

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['name', 'description', 'color']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def wikis_list_view(request, project_pk):
    project = Project.objects.get(pk=project_pk)

    context = {
        'wikis': Wiki.objects.filter(project=project),
        'project': project
    }

    return render(request, 'app/wiki_list.html', context)

class WikiDetailView(DetailView):
    model = Wiki

class WikiCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
    model = Wiki

    def get_success_url(self):
        wiki = self.get_object()
        return reverse_lazy('wiki-list', kwargs={'project_pk': wiki.project.id})

    def test_func(self):
        wiki = self.get_object()
        return self.request.user in wiki.project.contributors.all()

class WikiUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    return render(request, 'app/wikiversion_list.html', context)
