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
    return render(request, 'app/project/projects.html', context);

def labels(request):
    context = {
        'labels': Label.objects.all()
    }
    return render(request, 'app/label/label_list.html', context)

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
        return super().form_valid(form)

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
